import threading
import time

import requests
from scrapy_spider.common.ignore import douyin
from scrapy_spider.common.middleware.agent_manager import AgentManager

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

    def random_proxy(self):
        """随机代理"""
        # return random.choice(proxy_list)
        return None

    def filter_proxy_list(self, proxy_list):
        available_proxy_list = []
        for i in range(len(proxy_list)):
            proxy = proxy_list[i]
            print(f'检查第 {i} 个代理')
            if self.check_proxy_available(proxy):
                available_proxy_list.append(proxy)
        return available_proxy_list

    def filter_proxy_list_in_multi_thread(self, proxy_list):
        """TODO 需要限制线程数"""
        """过滤出可用的代理"""
        if not proxy_list:
            return []
        thread_list = []
        for i in range(len(proxy_list)):
            thread_list.append(ValidateProxyThread(i, self.check_proxy_available, proxy_list[i]))
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        available_proxy_list = []
        for proxy in proxy_list:
            if proxy['available']:
                available_proxy_list.append(proxy)
        return available_proxy_list

    def check_proxy_available(self, proxy) -> bool:
        """检查是否可用
        这个检查，如果直接用来爬取数据，也会非常好啊
        但是要注意防 ban"""
        ip, port, http_type = proxy['ip'], proxy['port'], proxy['http_type']
        http_type = http_type.lower()
        url = douyin.generate_feed_url(http_type=http_type)
        headers = {
            'user-agent': self.agent_manager.random_agent()
        }
        proxies = {
            http_type: f'{http_type}://{ip}:{port}'
        }
        timeout = 3
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                return self.extra_check(proxy, response)
            else:
                print('失败，状态码', response.status_code)
                pass
        except Exception as e:
            print('失败', e)
            pass
        return False

    def extra_check(self, proxy, response) -> bool:
        """额外的检查"""
        # TODO 这里可以保存抖音数据
        result = response.json()
        if result['status_code'] == 0:
            print('成功')
            proxy['available'] = 1
            return True
        else:
            proxy['available'] = 2
            proxy['banned_time'] = time.time()
            print('成功，但已被禁', result['status_code'])
            return True
