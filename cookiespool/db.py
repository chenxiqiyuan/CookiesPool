import random
import redis
from cookiespool.config import *

class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或Cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取数目
        :return: 数目
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.name())

import pymongo
class MongoDBClient(object):
    def __init__(self, type, website, host=MongoDB_HOST, port=MongoDB_PORT):
        """
        初始化 MongoDB 连接
        :param host: 地址
        :param port: 端口
        """
        self.type = type
        self.website = website
        self.db = pymongo.MongoClient(host=MongoDB_HOST, port=MongoDB_PORT)[self.website][self.type]

    def get_cookies(self, phone):
        """
        根据键名获取键值
        :param phone: 手机号
        :return: dict 形式的 手机号 和 cookies
        """
        result = self.db.find_one({'phone': phone}, {"_id": 0})
        return result

    def set_cookies(self, phone, cookies):
        """
        设置键值对
        :param username: 用户名
        :param value: dict 形式的 Cookies
        :return:
        """
        phone_cookies = {
        "phone":phone,
        "cookies":cookies
        }
        result = self.get_cookies(phone)
        print(result)
        if result == None:
            return self.db.insert_one(phone_cookies)
        else:
            return self.db.update_one(result, {'$set': phone_cookies})

if __name__ == '__main__':
    #conn = RedisClient('accounts', 'weibo')
    #result = conn.set('hell2o', 'sss3s')
    #print(result)

    conn = MongoDBClient('cookies', 'ele')
    my_ele = {
        "phone":"13626918317",
        "cookies":""
        }
    result = conn.db.insert_one(my_ele)
    print(result)