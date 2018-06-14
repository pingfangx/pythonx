# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import time

import scrapy
from scrapy_spider.common.log import log


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def generate_douyin_create_table_sql():
    """
    生成建表的 SQL
    :return:
    """
    item = AwemeItem()
    field_str = ''
    field_str += '"id" serial PRIMARY KEY NOT NULL,\n'

    pre_fields = {
        'aweme_id': 'text UNIQUE',
        'desc_': 'text',
        'statistics__digg_count': 'text',
        'statistics__comment_count': 'text',
        'video__play_addr__url_list__0': 'text',
        'crawl_time': 'text',
        'update_time': 'text',
        'crawled_times': 'int',
    }

    for key in pre_fields.keys():
        field_str += f'"{key}" {pre_fields[key]} NOT NULL,\n'

    for key in item.fields.keys():
        if key not in pre_fields.keys():
            field_str += f'"{key}" text NOT NULL,\n'
    # 去掉逗号
    field_str = field_str.rstrip(',\n')
    field_str += '\n'

    sql = f"CREATE TABLE IF NOT EXISTS {DOUYIN_TABLE_NAME} (\n{field_str});"
    return sql


def generate_douyin_insert_sql():
    """生成插入的 sql"""
    item = AwemeItem()
    # 列出名字
    fields_list = ', '.join(item.fields.keys())
    # 用 {} 包起来，后面用于格式化
    value_list = ', '.join(["'{%s}'" % k for k in item.fields.keys()])
    update_sql = 'crawled_times=EXCLUDED.crawled_times+1,'
    for key in item.fields.keys():
        if key.startswith('statistics__'):
            update_sql += "\n%s='{%s}'," % (key, key)
    update_sql += '\n%s={%s}' % ('update_time', 'update_time')

    sql = f'''
INSERT INTO {DOUYIN_TABLE_NAME} ({fields_list}) 
VALUES ({value_list})
ON CONFLICT(aweme_id) DO UPDATE SET
{update_sql};
'''
    return sql


class AwemeItem(scrapy.Item):
    crawl_time = scrapy.Field()
    """记录爬取时间"""

    update_time = scrapy.Field()
    """更新时间"""

    crawled_times = scrapy.Field()
    """爬取到的次数"""

    desc_ = scrapy.Field()
    """关键字，添加_"""

    create_time = scrapy.Field()
    is_ads = scrapy.Field()
    aweme_id = scrapy.Field()
    share_url = scrapy.Field()

    statistics__digg_count = scrapy.Field()
    statistics__comment_count = scrapy.Field()
    statistics__share_count = scrapy.Field()
    statistics__play_count = scrapy.Field()

    author__unique_id = scrapy.Field()
    author__short_id = scrapy.Field()
    author__uid = scrapy.Field()
    author__nickname = scrapy.Field()

    video__play_addr__url_list__0 = scrapy.Field()
    """数组，取 0"""

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 需要更新
        self['crawl_time'] = int(time.time())
        self['update_time'] = int(time.time())
        self['crawled_times'] = 1

        if data is not None:
            # 从 data 解析
            for k in self.fields.keys():
                groups = k.split('__')
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
                self[k] = ""


DOUYIN_TABLE_NAME = 'douyin'
DOUYIN_CREATE_TABLE_SQL = generate_douyin_create_table_sql()
DOUYIN_INSERT_SQL = generate_douyin_insert_sql()
