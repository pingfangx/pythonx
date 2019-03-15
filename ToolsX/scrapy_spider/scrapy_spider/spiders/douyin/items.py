import time

import scrapy

from scrapy_spider.common.item.base_item import BaseItem, BaseItemTest
from scrapy_spider.common.log import log


class DouyinItem(BaseItem):
    crawl_time_int4 = scrapy.Field()
    """记录爬取时间"""

    update_time_int4 = scrapy.Field()
    """更新时间"""

    crawled_times_int4 = scrapy.Field()
    """爬取到的次数"""

    desc_ = scrapy.Field()
    """关键字，添加_"""

    create_time_int4 = scrapy.Field()
    """拦音创建时间，覆盖了父类"""
    is_ads = scrapy.Field()
    aweme_id = scrapy.Field()
    share_url = scrapy.Field()

    statistics__digg_count_int4 = scrapy.Field()
    statistics__comment_count_int4 = scrapy.Field()
    statistics__share_count_int4 = scrapy.Field()
    statistics__play_count_int4 = scrapy.Field()

    author__short_id_int8 = scrapy.Field()
    author__uid_int8 = scrapy.Field()
    author__unique_id = scrapy.Field()
    author__nickname = scrapy.Field()

    video__play_addr__url_list__0 = scrapy.Field()
    """数组，取 0"""

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 需要更新
        self['crawl_time_int4'] = int(time.time())
        self['update_time_int4'] = int(time.time())

        if data is not None:
            # 从 data 解析
            for k in self.fields.keys():
                name, _type = self.parse_name_type(k)
                groups = name.split('__')
                # tmp 缩小
                tmp = data
                for i in range(len(groups) - 1):
                    tmp_key = groups[i].strip('_')
                    if tmp_key in tmp.keys():
                        tmp = tmp[tmp_key]
                    else:
                        log.warning('不存在 key ' + tmp_key)
                # 按名字取值
                final_key = groups[-1]
                # 用于一些关键字添加_
                final_key = final_key.strip('_')
                if isinstance(tmp, dict):
                    if final_key in tmp.keys():
                        value = tmp[final_key]
                        self[k] = value
                elif isinstance(tmp, list):
                    self[k] = tmp[int(final_key)]
        # 不为空
        for k in self.fields.keys():
            if k not in self.keys() or self[k] is None:
                name, _type = self.parse_name_type(k)
                if _type == 'text':
                    self[k] = ""
                else:
                    self[k] = 0

    def get_head_fields(self):
        return {
            'aweme_id': 'UNIQUE',
            'desc_': '',
            'statistics__digg_count_int4': '',
            'statistics__comment_count_int4': '',
            'share_url': '',
            'crawl_time_int4': '',
            'update_time_int4': '',
            'crawled_times_int4': '',
        }

    def get_tail_fields(self):
        return None

    def get_count_sql(self):
        """获取求数量的 sql"""
        return f"""
        SELECT COUNT(*) FROM {self.get_table_name()}
        """


class DouyinItemTest(BaseItemTest):
    item = DouyinItem()
