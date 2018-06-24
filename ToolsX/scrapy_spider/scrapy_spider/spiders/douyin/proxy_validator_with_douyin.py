import time

import requests
from scrapy_spider.common.ignore import douyin
from scrapy_spider.common.log import log
from scrapy_spider.spiders.douyin.items import DouyinItem
from scrapy_spider.spiders.douyin.pipelines import DouyinPostgreSQLPipeline


class ProxyValidatorWithDouyin:
    """ ip 校验，直接使用抖音校验"""
    items = []
    """item 好像不能在线程中保存，对 yield async 不熟悉
    先这样，线程中保存数据，执行完后再调用保存
    """

    def __init__(self):
        self.pipeline = DouyinPostgreSQLPipeline()
        # 初始化
        self.pipeline.open_spider(None)

    def validate_proxy(self, proxy) -> bool:
        """检查是否可用"""
        ip, port, http_type = proxy['ip'], proxy['port'], proxy['http_type']
        http_type = http_type.lower()
        url = douyin.generate_feed_url(http_type=http_type)
        headers = {
            'user-agent': douyin.generate_default_agent()
        }
        proxies = {
            http_type: f'{http_type}://{ip}:{port}'
        }
        timeout = 3
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                return self.validate_response(proxy, response.json())
            else:
                log.info(f'失败，请求状态码{response.status_code}')
                pass
        except Exception as e:
            log.info(f'失败{e}')
            pass
        return False

    def validate_response(self, proxy, result) -> bool:
        """从爬取代理的过程中，因为直接爬了抖音，所以解析数据"""
        status_code = result['status_code']
        if status_code == 0:
            aweme_list = result['aweme_list']
            proxy['available'] = 1
            log.info(f'代理有效，爬到 {len(aweme_list)} items')
            for aweme in aweme_list:
                item = DouyinItem(aweme)
                self.items.append(item)
            return True
        elif status_code == 2145:
            proxy['available'] = 2
            proxy['banned_time'] = time.time()
            log.info('代理有效，但已被禁', result['status_code'])
            return True

    def save_items(self):
        log.info(f'共爬取到 {len(self.items)} items，保存中')
        for item in self.items:
            self.pipeline.process_item(item, None)
        self.items.clear()
