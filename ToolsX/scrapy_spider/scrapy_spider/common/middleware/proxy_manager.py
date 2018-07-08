import queue
import random
import threading

from scrapy_spider.common.xx import threadx
from scrapy_spider.spiders.douyin.proxy_validator_with_douyin import ProxyValidatorWithDouyin

proxy_list = [
    {
        "anonymity": "透明",
        "area": "江西",
        "available": "True",
        "http_type": "HTTPS",
        "ip": "118.212.137.135",
        "port": "31288",
        "speed": "0.163秒",
        "survival_time": "138天"
    }
]


class ValidateProxyThread(threading.Thread):
    def __init__(self, thread_id, runnable, proxy):
        super().__init__()
        self.thread_id = thread_id
        self.runnable = runnable
        self.proxy = proxy

    def run(self):
        self.runnable(self.proxy)


class ProxyManager:

    def random_proxy(self):
        """随机代理"""
        return random.choice(proxy_list)


class ProxyFilter:
    """过滤"""

    def __init__(self, proxy_list):
        self._q = queue.Queue()
        self.available_q = queue.Queue()
        self.proxy_validator_with_douyin = ProxyValidatorWithDouyin()

        for proxy in proxy_list:
            self._q.put(proxy)

    def filter(self):
        multi_thread = threadx.HandleQueueMultiThread(self._q, callback=self.__filter_proxy, thread_num=10,
                                                      element_str_function=self.get_proxy_str, print_before_task=True)
        multi_thread.start()
        # 保存获取到的抖音
        self.proxy_validator_with_douyin.save_items()
        # 返回
        available_proxy = []
        while not self.available_q.empty():
            available_proxy.append(self.available_q.get())
        return available_proxy

    def __filter_proxy(self, element, element_index, thread_id):
        if self.proxy_validator_with_douyin.validate_proxy(element):
            self.available_q.put(element)

    @staticmethod
    def get_proxy_str(proxy):
        return f"{proxy['http_type']}://{proxy['ip']}:{proxy['port']}"
