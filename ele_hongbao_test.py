import json
from urllib.parse import urlparse,parse_qsl
import requests
from requests.exceptions import RequestException
import re
import time
import logging

#使用requests领取红包
#url = 'https://h5.ele.me/hongbao/?order_id=3051433848260702217&total_count=15&is_lucky_group=True&lucky_number=0&sn=2a58deeaf52eb009.2&theme_id=569'
def receive_hongbao_requests(url):
    try:
        headers = {"authority":"h5.ele.me",
"method":"POST",
"path":"/restapi/marketing/v2/promotion/weixin/211ED0F9EF27ECFB8D021BCB8B5638AF",
"scheme":"https",
"accept":"*/*",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9",
"content-length":"390",
"content-type":"text/plain;charset=UTF-8",
"dnt":"1",
"origin":"https://h5.ele.me",
"referer":url,
"sec-fetch-mode":"cors",
"sec-fetch-site":"same-origin",
"user-agent":"Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 V1_AND_SQ_5.3.1_196_YYB_D QQ/5.3.1.2335 NetType/WIFI",
"x-shard":"eosid=2116224313432584400;loc=118.096009,24.582285"
            }

        query=parse_qsl(urlparse(url)[4])
        data = {
	        "method": "phone",
	        "group_sn": query[4][1],
	        "sign": "b4a0964815aedd2bece64676012216b3",
	        "phone": "",
	        "platform": 0,
	        "track_id": "1570157471|2fd8d041d418ed2dfe292fb36a19304767c2cb1611da212c5a|d20eff3b42888ed24bb8b5c5635fb3b9",
	        "weixin_avatar": "http://thirdqq.qlogo.cn/g?b=oidb&k=xV4N9iaq11Vic0HLVZhXE1Lw&s=40&t=1557381617",
	        "weixin_username": "光",
	        "unionid": "fuck",
	        "latitude": "",
	        "longitude": ""
        }

        cookies = {
			'SID': 'UzCZP6BIkXFI5O4JNqHFtOmmTpU076eAVOAw', 
			'USERID': '117539558', 
			'UTUSER': '117539558', 
			'ZDS': '1.0|1574429613|YNTl3nLtNA7UIfscW8D+jS4Xe09s/xPIKPLm0QBTKH54LVbaMpIhHjpDyWAD5Yo0', 
			'track_id': '1574429613|49e6c624d49888c24c03b4a6a6ac1f9e0a54117745f7266c59|7c27f2dd1ad31a16c3770324d77d44fb'
            }

        #通过捕获警告到日志的方式忽略警告
        logging.captureWarnings(True)
        #SSL证书验证verify=False
        response = requests.post('https://h5.ele.me/restapi/marketing/v2/promotion/weixin/211ED0F9EF27ECFB8D021BCB8B5638AF', headers=headers, data=json.dumps(data), cookies = cookies, verify=False)

        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e.args)
        return None
    
def main():
    # 使用requests领取红包
    url = 'https://h5.ele.me/hongbao/?order_id=2118938891498873877&total_count=15&is_lucky_group=True&lucky_number=0&sn=1d67fbb1f88ce415.2&theme_id=569'
    html = receive_hongbao_requests(url)
    print(html)

if __name__ == '__main__':
    main()
    while True:
        time.sleep(10)