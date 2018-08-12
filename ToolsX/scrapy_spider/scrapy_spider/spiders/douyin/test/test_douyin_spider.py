from unittest import TestCase

from scrapy_spider.spiders.douyin.douyin_spider import DouyinSpider


class TestDouyinSpider(TestCase):
    def test_parse_time(self):
        list = [
            0,
            1,
            2,
            60,
            61,
            1439,
            1440,
            1441,
            10000,
        ]
        spider = DouyinSpider()
        for i in list:
            print(spider.parse_time(i))
