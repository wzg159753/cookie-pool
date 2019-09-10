# -*-coding:utf-8 -*-


import time, sys
from multiprocessing import Process

sys.path.append("E:\烟台所需\lwl_spider\proxies-master\proxies-master\proxies")

from api import app
from getter import Getter
from tester import Tester

# 周期
TESTER_CYCLE = 300
GETTER_CYCLE = 180

# 模块开关
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True


class Run:
    def run_tester(self, cycle=TESTER_CYCLE):
        """定时检测cookie可用情况"""
        tester = Tester()
        while True:
            print('开始检查')
            tester.run()
            time.sleep(cycle)

    def run_getter(self, cycle=GETTER_CYCLE):
        """定时获取cookie"""
        getter = Getter()
        while True:
            print('开始抓取cookies')
            getter.run()
            time.sleep(cycle)

    def run_api(self):
        """启动API接口"""
        app.run()

    def run(self):
        print('cookies池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.run_tester)
            tester_process.start()
        if GETTER_ENABLE:
            getter_process = Process(target=self.run_getter)
            getter_process.start()
        if API_ENABLE:
            api_process = Process(target=self.run_api)
            api_process.start()


if __name__ == '__main__':
    a = Run()
    a.run()
