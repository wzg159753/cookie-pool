# -*-coding:utf-8 -*-



import redis
from random import choice


# 分数设置
MAX_SCORE = 100
MIN_SCORE = 0
INIT_SCORE = 90

# 连接信息
REDIS_HOST = '192.168.1.52'
REDIS_PORT = 6379
# REDIS_PASSWORD = "a123456"
REDIS_PASSWORD = "xluniccc"

# REDIS_KEY = 'cookies'
CHECK_KEY = 'userpassword'

# 数据库最大存储的代理数量
POOL_UPPER_THRESHLD = 10000

# , passwd=REDIS_PASSWORD
class RedisClient:

    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT):
        """初始化redis对象"""
        self.db = redis.StrictRedis(host=host, port=port, db=14, password=REDIS_PASSWORD, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def add(self, REDIS_KEY, proxy, score=MAX_SCORE):

        """添加一个代理，设置初始分数"""
        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """首先随机获取最高分的有效cookie，不存在则按排名获取"""
        self.get().remove('accounts:tianyancha')
        key = choice(self.get())
        result = self.db.zrangebyscore(key, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            # 从分数前50的代理中随机获取一个
            result = self.db.zrevrange(key, 89, 100)
            if len(result):
                return choice(result)
            else:
                raise Exception('无可用cookies')

    def get_vip_proxy(self):
        """首先随机获取最高分的有效cookie，不存在则按排名获取"""
        keys = ["15853585853", "13022721916", "13375358581"]
        key = choice(keys)
        result = self.db.zrangebyscore(key, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            # 从分数前50的代理中随机获取一个
            result = self.db.zrevrange(key, 89, 100)
            if len(result):
                return choice(result)
            else:
                raise Exception('无可用cookies')

    def decrease(self, key, proxy):
        """代理分数-1，小于指定阈值则删除"""
        score = self.db.zscore(key, proxy)
        if score and score == MAX_SCORE:
            return self.db.delete(key)
        else:
            return self.db.delete(key)

    def max(self, key, proxy):
        """更新代理分数到最大值"""
        return self.db.zadd(key, {proxy: MAX_SCORE})

    def count(self):
        """获取代理数量"""
        keys = self.db.keys()
        counts = 0
        for key in keys:
            if "tianyancha" not in key:
                counts += self.db.zcard(key)
        return counts

    def all(self, key):
        """获取全部cookies"""
        return self.db.zrangebyscore(key, MIN_SCORE, MAX_SCORE)

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.name())

    def get_value(self, username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def get(self):
        """获取全部keys"""
        # print(self.db.keys())
        return self.db.keys()