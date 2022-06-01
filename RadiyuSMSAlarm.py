from email import message
import requests
import time
from json import loads
import json
import datetime
import uuid
import hmac
import hashlib
import platform
import asyncio



# 트위치에서 가져와야하는 값들
twitch_Application_ID = '!랜도프 트위치 클라이언트 ID를 입력해 주세요!!' 
twitch_Application_secret = '!랜도프 트위치 클라이언트 시크릿을 입력해 주세요 !!!'

#검색할 스트리머님의 ID
twitchID = 'radiyu' # !랜도프 해당 부분을 수정하면 다른 스트리머 님들의 알람을 받을수 있습니다.


# 아래 값은 필요시 수정 (일반적인 단순 문자 수신 상태에서는 수정할 필요는 없습니다.)
protocol = 'https'
domain = 'api.solapi.com'
prefix = ''

def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def get_headers(api_key, api_secret):
    date = get_iso_datetime()
    salt = unique_id()
    combined_string = date + salt
    return {
        'Authorization': 'HMAC-SHA256 ApiKey=' + api_key + ', Date=' + date + ', salt=' + salt + ', signature=' +
                         get_signature(api_secret, combined_string),
        'Content-Type': 'application/json; charset=utf-8'
    }

def get_url(path):
    url = '%s://%s' % (protocol, domain)
    if prefix != '':
        url = url + prefix
    url = url + path
    return url

def send_many(parameter):
    # 반드시 관리 콘솔 내 발급 받으신 API KEY, API SECRET KEY를 입력해주세요
    api_key = '!랜도프 솔라피 api 키를 입력해 주세요!!'
    api_secret = '!랜도프 솔라피 api 시크릿을 입력해 주세요!!!'
    parameter['agent'] = {
        'sdkVersion': 'python/4.2.0',
        'osPlatform': platform.platform() + " | " + platform.python_version()
    }

    return requests.post(get_url('/messages/v4/send-many'), headers=get_headers(api_key, api_secret), json=parameter)

oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_Application_ID + "&client_secret=" + twitch_Application_secret + "&grant_type=client_credentials")
access_token = loads(oauth_key.text)["access_token"]
token_type = 'Bearer '
Managerauthorization = token_type + access_token

a=0
if __name__ == '__main__':
    while True:
        print("봇이 방송을 기다리고 있습니다... 아 봇도 디유타임은 킹정이라 합니다.")

        Information = {'client-id': twitch_Application_ID, 'Authorization': Managerauthorization}
        api_response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + twitchID, headers=Information)
        print(api_response.text)
        

        try:            
            if loads(api_response.text)['data'][0]['type'] == 'live' and a == 0:
                print("뱅송 ON!!!")
                a = 1
                data = {
                'messages': [
                    {
                        'to': '01000000000',   # !랜도프 수신번호를 array로 입력하면 같은 내용을 여러명에게 보낼 수 있습니다.
                        'from': '01000000000',   # !랜도프 발신자 번호는 솔라피에 등록한 발신자 번호를 입력해주셔야 합니다.
                        'text': '전송할 내용을 입력해 주세요' # !랜도프 전송할 문자 메시지 내용입니다 ex)라디유 방송 ON!  
                    }
                ]
                }
                res = send_many(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        except:
            print("뱅송 off...")
            a = 0
        asyncio.sleep(15)
        time.sleep(5)