import unittest

from scrapy_spider.common.item.base_item import BaseItem
from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLHelper


class PostgreSQLHelperTest(unittest.TestCase):
    def test(self):
        self.test_transaction(False)

    def test_transaction(self, transaction=False):
        helper = PostgreSQLHelper(BaseItem())
        helper.transaction = transaction
        for i in range(helper.cached_commands_limit * 2 + 1):
            helper.insert_item(BaseItem())
        helper.close_connect()
