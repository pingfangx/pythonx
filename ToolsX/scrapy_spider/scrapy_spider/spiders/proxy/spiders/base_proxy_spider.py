import scrapy

from scrapy_spider.common.log import log
from scrapy_spider.spiders.proxy.filter.douyin_proxy_filter import DouyinProxyFilter


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
        'CONCURRENT_REQUESTS': 2,  # 并发影响不大，因为在校验时使用多线程程但是 join 了，在等待校验完毕
        'DOWNLOAD_DELAY': 1,  # 有并发，给 1 s 延时
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spider.common.middleware.middlewares.RandomAgentDownloaderMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.proxy.pipelines.ProxyPostgreSQLPipeline': 300,
        },
    }
    max_page = 0
    """最大页数"""

    ip_count = 1
    """平均抓取到的 ip 的数量，符点表示有效数 / 总数，如果为 0 ，说明已经失效"""

    def start_requests(self):
        if not self.max_page:
            self.max_page = 1
        page = 0
        while page < self.max_page:
            page += 1
            for i in range(len(self.start_urls)):
                url = self.start_urls[i]
                url = url.format(page=page)
                log.info(f'爬取第 {i+1}/{len(self.start_urls)} 个地址，第 {page}/{self.max_page} 页,{url}')
                yield scrapy.Request(url=url)

    def get_proxy_parser(self):
        """获取解析器"""
        return None

    def parse(self, response):
        proxy_parser = self.get_proxy_parser()
        if proxy_parser is None:
            return
        proxy_list = proxy_parser.parse_proxy_list_from_response(response)

        available_proxy_list = self.filter_proxy_list(proxy_list)
        for proxy in available_proxy_list:
            yield proxy

    def get_proxy_filter(self, proxy_list):
        """获取过滤器"""
        return DouyinProxyFilter(proxy_list)

    def filter_proxy_list(self, proxy_list):
        """过滤并保存代理"""
        log.info(f'抓取 {self.name} 共 {len(proxy_list)} 个代理，校验有效性')
        # 设置名字
        for proxy in proxy_list:
            proxy['source_domain'] = self.name

        # 每次都新建，各自过滤各自保存
        proxy_filter = self.get_proxy_filter(proxy_list)
        if proxy_filter is not None:
            available_proxy_list = proxy_filter.filter()
        else:
            available_proxy_list = proxy_list

        log.info(f'{self.name} 共 {len(available_proxy_list)}/{len(proxy_list)} 个代理有效')
        return available_proxy_list
