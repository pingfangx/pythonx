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


class AwemeItem(scrapy.Item):
    crawl_time = scrapy.Field()
    """记录爬取时间"""

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
        if data is None:
            return
        self['crawl_time'] = int(time.time())
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
