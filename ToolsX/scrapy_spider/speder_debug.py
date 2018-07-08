import unittest

from scrapy import cmdline


class SpiderTest(unittest.TestCase):

    def test_run_spider_to_json(self):
        spider = "douyin"
        args = "-o items.json"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())

    def test_run_spider(self):
        """运行抖音爬虫"""
        spider = "douyin"
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.douyin"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())

    def test_xicidaili_spider(self):
        self.test_proxy_spider('xicidaili')

    def test_data5u_spider(self):
        self.test_proxy_spider('data5u')

    def test_ip181_spider(self):
        self.test_proxy_spider('ip181')

    def test_kuaidaili_spider(self):
        self.test_proxy_spider('kuaidaili')

    def test_jiangxianli_spider(self):
        self.test_proxy_spider('jiangxianli')

    def test_iphai_spider(self):
        self.test_proxy_spider('iphai')

    def test_coderbusy_spider(self):
        self.test_proxy_spider('coderbusy')

    def test_goubanjia_spider(self):
        self.test_proxy_spider('goubanjia')

    def test_ip3366_spider(self):
        self.test_proxy_spider('ip3366')

    def test_66ip_spider(self):
        self.test_proxy_spider('66ip')

    def test_89ip_spider(self):
        self.test_proxy_spider('89ip')

    def test_swei360_spider(self):
        self.test_proxy_spider('swei360')

    def test_proxy_spider(self, spider):
        """运行代理爬虫"""
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.proxy.spiders"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())


if __name__ == '__main__':
    SpiderTest().test_run_spider()
