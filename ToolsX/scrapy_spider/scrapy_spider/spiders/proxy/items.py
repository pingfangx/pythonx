import scrapy

from scrapy_spider.common.item.base_item import BaseItem, BaseItemTest


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
        sql += f"source_domain='{self['source_domain']}',\n"
        # 如果重新爬取到，说明又是可以用的代理（需要校验时配合具体的使用地进行校验），置为 1
        # 0-1,1-1,2-2 其中 2 为被禁，仍然保留
        sql += "available=CEIL(ABS(EXCLUDED.available-0.5)),\n"
        sql += f"update_time={self['update_time']}"
        return sql

    def __str__(self):
        return f"{self['http_type']}://{self['ip']}:{self['port']}"

    def __setitem__(self, key, value):
        if key == 'http_type':
            # 最小写
            value = value.lower()
        super().__setitem__(key, value)

    @staticmethod
    def parse(proxy_str: str):
        """解析"""
        proxy_str = proxy_str.replace('/', '')
        http_type, ip, port = proxy_str.split(':')
        return ProxyItem(http_type=http_type, ip=ip, port=port)


class ProxyItemTest(BaseItemTest):
    item = ProxyItem()
