import scrapy


class PageItem(scrapy.Item):
    text = scrapy.Field()
    """内容"""

    path = scrapy.Field()
    """路径"""
