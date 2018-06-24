import threading

from scrapy_spider.common.middleware.agent_manager import AgentManager
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
    agent_manager = AgentManager()
    proxy_validator_with_douyin = ProxyValidatorWithDouyin()

    def random_proxy(self):
        """随机代理"""
        # return random.choice(proxy_list)
        return None

    def filter_proxy_list(self, proxy_list):
        available_proxy_list = []
        for i in range(len(proxy_list)):
            proxy = proxy_list[i]
            print(f'检查第 {i} 个代理')
            if self.validate_proxy(proxy):
                available_proxy_list.append(proxy)
        return available_proxy_list

    def filter_proxy_list_in_multi_thread(self, proxy_list):
        """TODO 需要限制线程数，而且还有数据的问题"""
        """过滤出可用的代理"""
        if not proxy_list:
            return []
        thread_list = []
        for i in range(len(proxy_list)):
            thread_list.append(ValidateProxyThread(i, self.validate_proxy, proxy_list[i]))
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        self.proxy_validator_with_douyin.save_items()
        available_proxy_list = []
        for proxy in proxy_list:
            if proxy['available']:
                available_proxy_list.append(proxy)
        return available_proxy_list

    def validate_proxy(self, proxy) -> bool:
        """检查 ip 可修改此方法"""
        return self.proxy_validator_with_douyin.validate_proxy(proxy)
