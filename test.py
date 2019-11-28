from cookiespool.generator import EleCookiesGenerator
from cookiespool.db import MongoDBClient
from cookiespool.api import *
import requests

def main():
    #app.run(host='0.0.0.0')

    #测试 ele 生成 cookie
    #conn = MongoDBClient('cookies', 'ele')
    #generator = EleCookiesGenerator()
    #result = generator.new_cookies("18866478774")
    #print(conn.set_cookies(result[0], result[1]))
    #print(result)

    #测试读取数据
    conn = MongoDBClient('cookies', 'ele')
    result = conn.get_cookies("18866478774")
    print(result)
    
    pass

if __name__ == '__main__':
    main()