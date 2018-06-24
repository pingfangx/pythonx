import scrapy
from lxml import etree
from scrapy_spider.common.log import log
from scrapy_spider.spiders.proxy.items import ProxyItem
from scrapy_spider.spiders.proxy.spiders.base_proxy_spider import BaseProxySpider


class XicidailiSpider(BaseProxySpider):
    name = "xicidaili"

    start_urls = [
        'http://www.xicidaili.com/wt/{page}',
        'http://www.xicidaili.com/wn/{page}',
    ]

    def start_requests(self):
        page = 0
        while page < 1:
            page += 1
            for url in self.start_urls:
                url = url.format(page=page)
                log.info("crawl " + url)
                yield scrapy.Request(url=url)

    def parse(self, response):
        selector = etree.HTML(response.text)
        tr_list = selector.xpath('//tr[@class="odd"]')
        proxy_list = []
        for info in tr_list:
            try:
                proxy_item = ProxyItem()
                proxy_item['ip'] = info.xpath('./td[2]/text()')[0]  # ip
                proxy_item['port'] = info.xpath('./td[3]/text()')[0]  # 端口
                area_list = info.xpath('./td[4]/a/text()')
                if area_list:
                    proxy_item['area'] = area_list[0]  # 地区，有可能为空，所以要判断
                proxy_item['anonymity'] = info.xpath('./td[5]/text()')[0]  # 匿名度
                proxy_item['http_type'] = info.xpath('./td[6]/text()')[0]  # 类型
                proxy_item['speed'] = info.xpath('./td[7]/div/@title')[0]  # 速度
                proxy_item['survival_time'] = info.xpath('./td[9]/text()')[0]  # 存活时间
                proxy_list.append(proxy_item)
            except Exception as e:
                log.error(e)
        available_proxy_list = self.filter_and_save_proxy_list(proxy_list)
        for proxy in available_proxy_list:
            yield proxy
