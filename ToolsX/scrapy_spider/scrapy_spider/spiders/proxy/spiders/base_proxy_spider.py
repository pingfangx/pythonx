import scrapy

from scrapy_spider.common.log import log
from scrapy_spider.common.middleware.proxy_manager import ProxyFilter


class BaseProxySpider(scrapy.Spider):
    """代理爬虫基类
    一开始找到的 https://github.com/monkey-soft/Scrapy_IPProxyPool，开始写爬代理的爬虫
    后来在 github 搜代理，找出更多爬虫与代理网站

    架构为
    不同的 spider 爬取
    然后将给 proxy_parser 解析出代理
    再交由 ProxyFilter 过滤出有效的代理
    过滤时先使用 telnet 判断是否有效，再使用 ProxyValidatorWithDouyin 直接抓抖音进行校验

    代理的解析，一开始用的 xpath 解析，觉得麻烦就简单提取，后来发现用正则匹配更简单
    """

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spider.common.middleware.middlewares.RandomAgentDownloaderMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.proxy.pipelines.ProxyPostgreSQLPipeline': 300,
        },
    }
    max_page = 0
    """最大页数"""

    def start_requests(self):
        if not self.max_page:
            self.max_page = 1
        page = 0
        while page < self.max_page:
            page += 1
            for url in self.start_urls:
                url = url.format(page=page)
                log.info("crawl " + url)
                yield scrapy.Request(url=url)

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    def filter_and_save_proxy_list(self, proxy_list):
        """过滤并保存代理"""
        log.info(f'抓取 {self.name} 共 {len(proxy_list)} 个代理，校验有效性')
        available_proxy_list = ProxyFilter(proxy_list).filter()
        log.info(f'{self.name} 共 {len(available_proxy_list)} 个代理有效')
        return available_proxy_list
