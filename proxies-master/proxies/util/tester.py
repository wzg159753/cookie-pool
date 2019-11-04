# -*-coding:utf-8 -*-
import asyncio
import aiohttp
import time
from lxml import etree
import requests
from schedule.db import RedisClient


# 目标网址
# TEST_URL = 'https://www.tianyancha.com/company/2357560244'
TEST_URL = 'https://www.tianyancha.com/usercenter/myorder'
# 正确的响应码列表
TRUE_STATUS_CODE = [200]
# 同时测试一组代理的数量
BATCH_TEST_SIZE = 20


class Tester:

    def __init__(self, website='tianyancha'):
        """初始化数据库管理对象"""
        self.website = website
        self.redis = RedisClient('accounts', self.website)

    async def test_one_proxy(self, key, proxy):
        """对目标网站测试一个cookies是否可用"""
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # 解码为字符串
                headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Cookie": proxy[:-1],
                        "Host": "www.tianyancha.com",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

                # async with session.get(TEST_URL, headers=headers, timeout=30) as response:
                try:
                    response = requests.get(TEST_URL, headers=headers, timeout=30)
                    result = response.text
                    html = etree.HTML(result)
                    # print("".join(html.xpath('//div[@class="box -company-box "]/div[@class="content"]/div[@class="header"]/h1[@class="name"]/text()')))
                    user = "".join(html.xpath('//span[@class="ni-sp-name"]//text()'))
                    print(user, '*'*20)
                    """"".join(html.xpath('//div[@class="box -company-box "]/div[@class="content"]/div[@class="header"]/h1[@class="name"]/text()'))"""
                    if response.status_code in TRUE_STATUS_CODE and user:
                        # cookie可用
                        self.redis.max(key, proxy)
                        print(key, 100, '可用')
                    else:
                        # cookie不可用
                        # send = Send_Click()
                        # staus = send.run(proxy)
                        # if staus:
                        #     self.redis.max(key, proxy)
                        #     print(key, 100, "通过点字验证")
                        # else:
                        a = self.redis.decrease(key, proxy)
                        print(key, -20, "状态码错误")
                except Exception as e:
                    print(key, '请求错误', -20, e)
            except Exception as e:
                # self.redis.decrease(key, proxy)
                print(key, '测试错误', -20, e)

    async def start(self):
        """启动协程， 测试所有cookies"""
        try:
            keys = self.redis.get()
            for key in keys:
                if "tianyancha" not in key:
                    proxies = self.redis.all(key)
                    print(key)
                    for i in range(0, len(proxies)):
                        test_proxies = proxies[i: i+BATCH_TEST_SIZE]
                        tasks = [self.test_one_proxy(key,proxy) for proxy in test_proxies]
                        asyncio.gather(*tasks)
                        time.sleep(5)
                else:
                    pass
        except Exception as e:
            print('测试器发生错误', e.args)

    def run(self):
        asyncio.run(self.start())
        # # python3.7之前的写法
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.start())

if __name__ == '__main__':
    a = Tester()
    a.run()


