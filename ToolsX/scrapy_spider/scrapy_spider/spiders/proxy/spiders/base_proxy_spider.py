import scrapy
from scrapy_spider.common.log import log
from scrapy_spider.common.middleware.proxy_manager import ProxyManager


class BaseProxySpider(scrapy.Spider):
    """代理爬虫基类
    参考 https://github.com/monkey-soft/Scrapy_IPProxyPool
    感谢
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

    proxy_manager = ProxyManager()

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    def filter_and_save_proxy_list(self, proxy_list):
        """过滤并保存代理"""
        log.info(f'抓取 {self.name} 共 {len(proxy_list)} 个代理，校验有效性')
        available_proxy_list = self.proxy_manager.filter_proxy_list_in_multi_thread(proxy_list)
        log.info(f'{self.name} 共 {len(available_proxy_list)} 个代理有效')
        return available_proxy_list
