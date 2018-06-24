import scrapy
from scrapy_spider.common.item.base_item import BaseItem


class ProxyItem(BaseItem):
    """代理"""
    source_domain = scrapy.Field()
    """来源网站"""

    ip = scrapy.Field()
    """ip"""

    port = scrapy.Field()
    """端口"""

    anonymity = scrapy.Field()
    """匿名度"""

    http_type = scrapy.Field()
    """类型"""

    banned_time_int4 = scrapy.Field()
    """被禁时间"""

    area = scrapy.Field()
    """地区"""

    speed = scrapy.Field()
    """速度"""

    survival_time = scrapy.Field()
    """匿名度"""

    available = scrapy.Field()
    """是否可用"""

    def get_head_fields(self):
        return {
            'http_type': '',
            'ip': 'UNIQUE',
            'port': '',
            'banned_time_int4': '',
            'available': '',
        }
