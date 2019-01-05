import unittest

import scrapy

from scrapy_spider.common.item.base_item import BaseItem


class WeiboVideoItem(BaseItem):
    author = scrapy.Field()
    """作者"""

    comment = scrapy.Field()
    """评论数"""

    content = scrapy.Field()
    """内容"""

    keyword = scrapy.Field()
    """搜索时使用的关键字"""

    video_url = scrapy.Field()
    """视频地址"""


class ItemTest(unittest.TestCase):
    item = WeiboVideoItem()

    def test_generate_create_table_sql(self):
        print(self.item.generate_create_table_sql())

    def test_generate_insert_formatter_sql(self):
        print(self.item.generate_insert_formatter_sql())
