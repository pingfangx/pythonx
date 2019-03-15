import time

import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from scrapy_spider.common.log import log
from scrapy_spider.spiders.douyin import douyin_spider
from scrapy_spider.spiders.douyin.ignore import douyin
from scrapy_spider.spiders.douyin.items import DouyinItem
from scrapy_spider.spiders.douyin.pipelines import DouyinPostgreSQLPipeline
from scrapy_spider.spiders.proxy.validator.base_proxy_validator import BaseProxyValidator


class DouyinProxyValidator(BaseProxyValidator):
    """抖音代理校验"""

    items = []
    """item 好像不能在线程中保存，对 yield async 不熟悉
    先这样，线程中保存数据，执行完后再调用保存
    """

    def __init__(self):
        super().__init__(timeout=5)
        self.pipeline = DouyinPostgreSQLPipeline()
        # 初始化
        self.pipeline.open_spider(None)

    def validate(self, proxy):
        ip, port, http_type = proxy['ip'], proxy['port'], proxy['http_type']
        proxy_url = f'{http_type}://{ip}:{port}'

        http_type = http_type.lower()
        anonymous = douyin_spider.ANONYMOUS
        url = douyin.generate_feed_url(http_type=http_type, anonymous=anonymous)
        proxies = {
            http_type: proxy_url
        }
        result = False
        response = None
        try:
            headers = douyin.generate_headers(anonymous)
            cookies = douyin.generate_cookies(anonymous)
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=self.timeout,
                                    verify=False)
            if response.status_code == 200:
                try:
                    result = self.validate_response(proxy, response.json())
                except Exception as e:
                    # print(f'{proxy}-解析出错 {e}')
                    pass
            else:
                # print(f'{proxy}-失败，请求状态码{response.status_code}')
                pass
        except (ConnectTimeout, ConnectionError, ReadTimeout) as e:
            # print(f'{proxy}-连接超时 {e}')
            pass
        except Exception as e:
            # log.info(f'{proxy}-失败{type(e)}{e}')
            pass
        if response:
            response.close()
        return result

    def validate_response(self, proxy, result) -> bool:
        """从爬取代理的过程中，因为直接爬了抖音，所以解析数据"""
        status_code = result['status_code']
        if status_code == 0:
            aweme_list = result['aweme_list']
            proxy['available'] = 1
            log.info(f'{proxy}-代理有效，爬到 {len(aweme_list)} items')
            for aweme in aweme_list:
                item = DouyinItem(aweme)
                self.items.append(item)
            return True
        elif status_code == 2154:
            proxy['available'] = 2
            proxy['banned_time'] = time.time()
            log.info(f"{proxy}-代理有效，但已被禁{result['status_code']}")
            return True
        else:
            print(f"{proxy}-代理无效，返回状态码{result['status_code']}")
            return False

    def save_items(self):
        log.info(f'共爬取到 {len(self.items)} items，保存中')
        for item in self.items:
            self.pipeline.process_item(item, None)
        self.items.clear()
        self.pipeline.close_spider(None)
