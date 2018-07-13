import json
import time

import scrapy
from scrapy_spider.common.ignore import douyin  # 不公开
from scrapy_spider.common.log import log
from scrapy_spider.spiders.douyin.items import DouyinItem


class statistics:
    """统计"""

    start_time = 0
    """开始时间"""
    crawled_pages = 0
    """爬取页数"""
    crawled_success__pages = 0
    """爬取成功页数"""
    crawled_items = 0
    """爬取抖音数"""


CONCURRENT_REQUESTS = 16
"""并发数"""


class DouyinSpider(scrapy.Spider):
    """
    参考 https://github.com/a232319779/appspider
    感谢
    爬取速度
    并发  速度
    16  800
    """
    name = 'douyin'

    # 防 ban
    custom_settings = {
        'CONCURRENT_REQUESTS': CONCURRENT_REQUESTS,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 10,  # 设置超时，默认是 180
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy_spider.common.middleware.middlewares.RandomAgentDownloaderMiddleware': 300,
            'scrapy_spider.common.middleware.middlewares.DouyinRandomProxyDownloaderMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.douyin.pipelines.DouyinPostgreSQLPipeline': 300,
        },
    }
    # 好像使用 user-agent 标识，所以保持不变
    headers = {
        'user-agent': douyin.generate_default_agent(),
    }
    has_more = 1
    exit_code = 1
    statistics = statistics()

    def start_requests(self):
        self.statistics.start_time = time.time()
        i = 0
        while i < 1:
            # i += 1
            # 并发的时候，time 是相同的，被 scrapy 认为是相同地址而忽略
            # 后来发现要设置 dont_filter
            url = douyin.generate_feed_url()
            self.statistics.crawled_pages += 1
            log.info(f'crawl {self.statistics.crawled_pages} page:' + url)
            yield scrapy.Request(url=url, headers=self.headers, dont_filter=True)
            if self.has_more == 0 or self.exit_code == 0:
                break

    def parse(self, response):
        try:
            body = response.body.decode()
            if body == 'error':
                print('body 为 error，异常已拦截')
                return
            result = json.loads(body)
            status_code = result['status_code']
            if result['status_code'] == 0:
                self.has_more = result['has_more']
                aweme_list = result['aweme_list']
                self.statistics.crawled_success__pages += 1
                self.statistics.crawled_items += len(aweme_list)
                minute = (time.time() - self.statistics.start_time) / 60
                print(f'scraped {len(aweme_list)} items')
                speed = self.statistics.crawled_items / minute
                log.info(
                    f'scraped {self.statistics.crawled_success__pages}/{self.statistics.crawled_pages} pages,'
                    f'{self.statistics.crawled_items} items,spend {minute:#.2f} minutes,speed {speed:#.2f} items/min')
                for aweme in aweme_list:
                    item = DouyinItem(aweme)
                    yield item
            elif status_code == 2145:
                log.warning('请求已过期')
                self.exit_code = 0
            elif status_code == 2151:
                log.warning('签名错误')
                self.exit_code = 0
            elif status_code == 2154:
                # 大约会被禁 1 个小时
                # 已经在下载器中间件拦截，应该不会走到这里的
                log.warning('请求太频繁，设备被禁')
                # log.warning('休息 10 分钟')
                # self.sleep_time = 10 * 60
                # self.exit_code = 0
            else:
                log.warning('错误码 %d' % status_code)
                log.warning(response.body.decode())
                self.exit_code = 0
        except Exception as e:
            # TODO 这里要解析代理出错，或者在中间件里处理
            log.error('出错了')
            log.error(repr(e))
