'''
@Description: 进行项目测试
@Author: chenxi
@Date: 2019-11-01 16:15:21
@LastEditTime: 2019-11-29 19:49:12
@LastEditors: chenxi
'''
from cookiespool.generator import EleCookiesGenerator
from cookiespool.db import MongoDBClient
from cookiespool.api import *
import requests
from ele_action import *
import ele_action

def main():
    # 领取红包
    # phone = "19859215155"
    # url = 'https://h5.ele.me/hongbao/?order_id=2118938891498873877&total_count=15&is_lucky_group=True&lucky_number=0&sn=1d67fbb1f88ce415.2&theme_id=569'
    # ele_action.main(phone, url)
    # 测试flask
    # app.run(host='0.0.0.0')
    # 运行饿了么生成器
    generator = EleCookiesGenerator()
    generator.run()

    pass


if __name__ == '__main__':
    main()
