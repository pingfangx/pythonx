import scrapy

from scrapy_spider.common.item.base_item import BaseItem, BaseItemTest


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


class WeiboVideoItemTest(BaseItemTest):
    item = WeiboVideoItem()
