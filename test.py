from cookiespool.generator import EleCookiesGenerator
from cookiespool.db import MongoDBClient
import requests
def main():
    #测试 ele 生成 cookie 
    #conn = MongoDBClient('cookies', 'ele')
    #generator = EleCookiesGenerator()
    #result = generator.new_cookies("13626918317")
    #print(conn.set_cookies(result[0], result[1]))
    #print(result)
    #result = generator.new_cookies("19859215155")
    #print(conn.set_cookies(result[0], result[1]))
    #print(result)

    #测试读取数据
    #conn = MongoDBClient('cookies', 'ele')
    #result = conn.get_cookies("13626918317")
    #print(result)

if __name__ == '__main__':
    main()