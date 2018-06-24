import asyncio

from scrapy_spider.common.item.base_item import BaseItem
from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLManager


class BasePostgreSQLPipeline(object):
    """现在是直接保存，可以优化为批量保存"""
    item = BaseItem

    def __init__(self):
        self.manager = self.get_postgresql_manager()

    def get_postgresql_manager(self):
        item = self.item()
        return PostgreSQLManager(item)

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
        asyncio.get_event_loop().run_until_complete(self.manager.connect_database())
        asyncio.get_event_loop().run_until_complete(self.manager.create_table())

    def close_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(self.manager.close_connect())

    def process_item(self, item, spider):
        asyncio.get_event_loop().run_until_complete(self.manager.insert_item(item))
        return item
