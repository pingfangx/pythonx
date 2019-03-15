import asyncio
import json
import time

import scrapy
from scrapy_spider.common.log import log
from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLManager
from scrapy_spider.spiders.douyin.ignore import douyin  # 不公开
from scrapy_spider.spiders.douyin.items import DouyinItem

ANONYMOUS = False
"""
是否匿名
如果匿名，可以更快的爬取数据，但是遗憾的是，因为没有身份标识，会爬取到重复的数据
之前也有考虑到身份标识这个问题，一开始以为是用的 user-agent，爬取了几次数据都没重复，就没在意，
没想到爬取的数量多了之后重复就明显了

如果不匿名，会拼接完整的请求参数，并设置 cookies，目前也不知道是通过参数还是 cookeis 判断的
"""

CONCURRENT_REQUESTS = 16 if ANONYMOUS else 1
"""并发数
匿名为 16，不匿名为 1"""

DOWNLOAD_DELAY = 0 if ANONYMOUS else 10
"""爬取延时
匿名为 0，不匿名为 10"""


class Statistics:
    """统计"""

    start_time = 0
    """开始时间"""
    start_craw_count = 0
    """开始爬取时的数量"""
    crawled_pages = 0
    """爬取页数"""
    crawled_success__pages = 0
    """爬取成功页数"""
    crawled_items = 0
    """爬取抖音数"""
    few_available_result_times = 0
    """爬取结果中有效数量较少的次数"""


class DouyinPostgreSQLManager(PostgreSQLManager):
    """数据库管理"""

    def __init__(self):
        item = DouyinItem()
        super().__init__(item)
        asyncio.get_event_loop().run_until_complete(self.prepare())
        self._sql_count = item.get_count_sql()

    def count(self):
        return asyncio.get_event_loop().run_until_complete(self.conn.fetchval(self._sql_count))


class DouyinSpider(scrapy.Spider):
    """
    参考 https://github.com/a232319779/appspider
    感谢
    爬取速度
    scraped 29295/29533 pages,186375/454024 items,spend 12927.06 minutes,speed 35.12 items/min,
    scraped 42849/43301 pages,315094/834373 items,spend 18150.73 minutes,speed 45.97 items/min,
    scraped 22803/23147 pages,108139/200390 items,spend 7 days 23:33,speed 17.44 items/min,
     scraped 21560/22027 pages,98100/134050 items,spend 7 days 10:58,speed 12.48 items/min.
     scraped 70505/75185 pages,335239/448673 items,spend 17 days 12:35,speed 17.78 items/min.
    """
    name = 'douyin'
    downloader_middlewares = {
        # 'scrapy_spider.common.middleware.middlewares.RandomAgentDownloaderMiddleware': 300,
        'scrapy_spider.common.middleware.middlewares.DouyinRandomProxyDownloaderMiddleware': 300,
    }
    # 防 ban
    custom_settings = {
        'CONCURRENT_REQUESTS': CONCURRENT_REQUESTS,
        'DOWNLOAD_DELAY': DOWNLOAD_DELAY,
        'DOWNLOAD_TIMEOUT': 10,  # 设置超时，默认是 180
        'DOWNLOADER_MIDDLEWARES': downloader_middlewares,
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.douyin.pipelines.DouyinPostgreSQLPipeline': 300,
        },
    }
    sleep_time = 1
    has_more = 1
    exit_code = 1
    statistics = Statistics()
    manager = DouyinPostgreSQLManager()

    def start_requests(self):
        self.statistics.start_time = time.time()
        i = 0
        self.statistics.start_craw_count = self.manager.count()
        log.info(f'爬取前 item 数量 {self.statistics.start_craw_count}')
        while i < 1:
            # i += 1
            if not ANONYMOUS:
                log.info(f'sleep {self.sleep_time}')
                time.sleep(self.sleep_time)
                self.sleep_time = 1
            # 并发的时候，time 是相同的，被 scrapy 认为是相同地址而忽略
            # 后来发现要设置 dont_filter
            anonymous = ANONYMOUS
            url = douyin.generate_feed_url('http', anonymous)
            headers = douyin.generate_headers(anonymous)
            cookies = douyin.generate_cookies(anonymous)
            self.statistics.crawled_pages += 1
            log.info(f'crawl {self.statistics.crawled_pages} page:' + url)
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, dont_filter=True)
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
                # 之前的数量
                before_item_count = self.manager.count()
                for aweme in aweme_list:
                    item = DouyinItem(aweme)
                    yield item
                # 保存后再统计
                # 之后的数量
                current_item_count = self.manager.count()
                self.statistics.crawled_success__pages += 1
                self.statistics.crawled_items += len(aweme_list)
                minute = (time.time() - self.statistics.start_time) / 60
                available_count = current_item_count - before_item_count
                if available_count <= 2:
                    # 获取数量较小，需要等待
                    if self.statistics.few_available_result_times >= 5:
                        self.statistics.few_available_result_times = 0
                        log.info('有 5 次抓取到的有效结果都较少，等待 600 s')
                        self.sleep_time = 600
                    else:
                        self.statistics.few_available_result_times += 1
                        log.info('抓取到的有效结果较少，等待 60s')
                        self.sleep_time = 60
                else:
                    self.statistics.few_available_result_times = 0
                log.info(f'scraped {len(aweme_list)} items,available {available_count} items.')
                speed = self.statistics.crawled_items / minute
                log.info(
                    f'scraped {self.statistics.crawled_success__pages}/{self.statistics.crawled_pages} pages,'
                    f'{current_item_count - self.statistics.start_craw_count}/{self.statistics.crawled_items} items,'
                    f'spend {self.parse_time(minute)},speed {speed:#.2f} items/min.')
            elif status_code == 2145:
                log.warning('请求已过期')
                self.exit_code = 0
            elif status_code == 2151:
                log.warning('签名错误')
                self.exit_code = 0
            elif status_code == 2154:
                # 大约会被禁 1 个小时
                log.warning('请求太频繁，设备被禁')
                if ANONYMOUS:
                    # 已经在下载器中间件拦截，应该不会走到这里的
                    pass
                else:
                    # 不匿名需要处理
                    log.warning('休息 10 分钟')
                    self.sleep_time = 10 * 60
                    # 仅休眠，不退出
                    # self.exit_code = 0
            else:
                log.warning('错误码 %d' % status_code)
                log.warning(response.body.decode())
                self.exit_code = 0
        except Exception as e:
            # TODO 这里要解析代理出错，或者在中间件里处理
            log.error('出错了')
            log.error(repr(e))

    @staticmethod
    def parse_time(minute):
        minute = int(minute)
        """显示分钟"""
        if minute < 60 * 24:
            hour = int(minute / 60)
            minute = minute % 60
            return f'{hour:#02d}:{minute:#02d}'
        else:
            day = int(minute / 1440)
            hour = int((minute % 1440) / 60)
            minute = minute % 60
            plural = 's' if day > 1 or day == 0 else ''
            return f'{day} day{plural} {hour:#02d}:{minute:#02d}'
