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

    def test_proxy_spider(self):
        """运行代理爬虫"""
        spider = "xicidaili"
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.proxy.spiders"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())


if __name__ == '__main__':
    SpiderTest().test_run_spider()
