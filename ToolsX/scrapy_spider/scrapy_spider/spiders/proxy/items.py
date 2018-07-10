import scrapy
from scrapy_spider.common.item.base_item import BaseItem


class ProxyItem(BaseItem):
    """代理"""
    source_domain = scrapy.Field()
    """来源网站"""

    used_times_int4 = scrapy.Field()
    """使用次数"""

    success_times_int4 = scrapy.Field()
    """成功次数"""

    fail_times_int4 = scrapy.Field()
    """失败次数"""

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

    available_int4 = scrapy.Field()
    """是否可用
    0 失效
    1 有效
    2 被禁
    """

    def get_head_fields(self):
        return {
            'http_type': '',
            'ip': 'UNIQUE',
            'port': '',
            'banned_time_int4': '',
            'available_int4': '',
            'used_times_int4': '',
            'success_times_int4': '',
            'fail_times_int4': '',
        }

    def get_on_conflict_suffix_sql(self):
        """多更新一下来源"""
        sql = f"""
        ON CONFLICT(ip) DO UPDATE SET
        crawled_times={self.get_table_name()}.crawled_times+1,
        """
        sql += "source_domain='{source_domain}',\n"
        sql += 'update_time={update_time_int4}'
        return sql

    def __str__(self):
        return f"{self['http_type']}://{self['ip']}:{self['port']}"
