'''
@Description: 饿了么动作
@Author: chenxi
@Date: 2019-09-30 15:18:39
@LastEditTime: 2019-11-29 19:50:45
@LastEditors: chenxi
'''
import json
from urllib.parse import urlparse, parse_qsl
import requests
from requests.exceptions import RequestException
import re
import time
import logging
from cookiespool.db import MongoDBClient
from cookiespool.generator import EleCookiesGenerator


def DailyPrize(cookies, longitude="118.09600867331007", latitude="24.58228485658733"):
    '''
    @description: 每日签到奖励
    @param : 
    @return: 
    '''
    try:
        headers = {
            "Host": "h5.ele.me",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://tb.ele.me",
            "x-shard": "loc="+longitude+","+latitude,
            "User-Agent": "Rajax/1 Redmi_Note_4/lineage_mido Android/4.4.2 Display/lineage_mido-user_4.4.2_NJH47F_380180120_release-keys Eleme/8.0.0 Channel/moxiu ID/05d52983-2dd7-3182-8b6f-352b8d10b426; KERNEL_VERSION:3.4.0 API_Level:19 Hardware:9372d36c420782c17b7d23de3634ee9e Mozilla/5.0 (Linux; Android 4.4.2; Redmi Note 4 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://tb.ele.me/wow/zele/act/qiandao?wh_biz=tm&activity_ids=%5B10817194%5D&source=main",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "me.ele"
        }
        data = {"channel": "app", "index": 2,
                "longitude": longitude, "latitude": latitude}
        url = "https://h5.ele.me/restapi/member/v2/users/2000032867700/sign_in/daily/prize"
        # 通过捕获警告到日志的方式忽略警告
        logging.captureWarnings(True)
        # SSL证书验证verify=False
        response = requests.post(url, headers=headers, data=json.dumps(
            data), cookies=cookies, verify=False)
        return response.text
    except RequestException as e:
        print(e.args)
        return None


def receive_hongbao(url, cookies):
    '''
    @description: 领取红包
    @param : url : 红包链接
    @return: cookies : 用户 cookies
    '''
    try:
        headers = {"authority": "h5.ele.me",
                   "method": "POST",
                   "path": "/restapi/marketing/v2/promotion/weixin/211ED0F9EF27ECFB8D021BCB8B5638AF",
                   "scheme": "https",
                   "accept": "*/*",
                   "accept-encoding": "gzip, deflate, br",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "content-length": "390",
                   "content-type": "text/plain;charset=UTF-8",
                   "dnt": "1",
                   "origin": "https://h5.ele.me",
                   "referer": url,
                   "sec-fetch-mode": "cors",
                   "sec-fetch-site": "same-origin",
                   "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 V1_AND_SQ_5.3.1_196_YYB_D QQ/5.3.1.2335 NetType/WIFI",
                   "x-shard": "eosid=2116224313432584400;loc=118.096009,24.582285"
                   }

        query = parse_qsl(urlparse(url)[4])
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

        # 通过捕获警告到日志的方式忽略警告
        logging.captureWarnings(True)
        # SSL证书验证verify=False
        response = requests.post('https://h5.ele.me/restapi/marketing/v2/promotion/weixin/211ED0F9EF27ECFB8D021BCB8B5638AF',
                                 headers=headers, data=json.dumps(data), cookies=cookies, verify=False)
        return response.text
    except RequestException as e:
        print(e.args)
        return None


def main(url, phone):
    # 初始化
    conn = MongoDBClient('cookies', 'ele')
    cookies = conn.get_cookies(phone)
    if cookies == None:
        # 生成 cookie
        generator = EleCookiesGenerator()
        cookies = generator.new_cookies(phone)
        if cookies == None:
            return
        print(conn.set_cookies(cookies['phone'], cookies['cookies']))

    # 领取红包
    # html = receive_hongbao(url, cookies['cookies'])
    # print(html)
    # if "message" in json.loads(html) and json.loads(html)["message"] == "未登录":
    #     print(conn.del_cookies(phone))
    # 每日签到
    # result = DailyPrize(cookies['cookies'])
    # print(result)


if __name__ == '__main__':
    url = 'https://h5.ele.me/hongbao/?order_id=3055075640043320379&total_count=15&is_lucky_group=True&lucky_number=0&sn=2a65cf1baebb343b.2&theme_id=569'
    # phone = "18866478774"
    phone = "19859215155"
    main(url, phone)
    # while True:
    #     time.sleep(10)
