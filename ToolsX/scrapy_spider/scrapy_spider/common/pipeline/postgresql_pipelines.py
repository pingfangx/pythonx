import unittest

from scrapy_spider.common.item.base_item import BaseItem
from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLHelper
from scrapy_spider.spiders.ignore.downloader.items import NineItem


class BasePostgreSQLPipeline(object):
    """现在是直接保存，可以优化为批量保存"""
    item: BaseItem = BaseItem()

    update = False
    """是否是更新"""

    def __init__(self):
        self.helper: PostgreSQLHelper = PostgreSQLHelper(self.item)

    @staticmethod
    def camel_to_under_line(text):
        result = ''
        for i in range(len(text)):
            c = text[i]
            if c.isupper():
                if i != 0:
                    result += '_'
                result += c.lower()
            else:
                result += c
        return result

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.helper.close_connect()

    def process_item(self, item, spider):
        if isinstance(item, NineItem):
            if self.update:
                self.helper.update_item(item)
            else:
                self.helper.insert_item(item)
        return item


class BasePostgreSQLPipelineTest(unittest.TestCase):
    pipeline: BasePostgreSQLPipeline = BasePostgreSQLPipeline()
    insert_item: BaseItem = None

    def test_create_table(self):
        self.pipeline.open_spider(None)

    def test_insert(self):
        if self.insert_item:
            self.pipeline.open_spider(None)
            self.pipeline.process_item(self.insert_item, None)
