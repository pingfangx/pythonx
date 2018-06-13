# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import asyncio
import copy
import json

import asyncpg
from scrapy_spider.ignore.postgreconfig import postgre_configs


class FilePipeline(object):
    """保存为文件"""

    file = None
    """文件"""

    def open_spider(self, spider):
        self.file = open(spider.name + '.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class PostgreSQLPipeline(object):
    def __init__(self):
        self.sql_create_table = ''
        self.sql_insert_item = ''
        self.conn = None

        self.items_cache = []
        self.cache_threshold = 0

        self.table_name = 'douyin'
        # 这里的sql 语句不区分大小写，如果用大写字母命名表名会报错
        self.sql_create_table = f'''
CREATE TABLE IF NOT EXISTS {self.table_name} (
"id" serial PRIMARY KEY NOT NULL,
"author__nickname" text NOT NULL,
"author__short_id" text NOT NULL,
"author__uid" text NOT NULL,
"author__unique_id" text NOT NULL,
"aweme_id" text NOT NULL,
"crawl_time" text NOT NULL,
"create_time" text NOT NULL,
"desc_" text NOT NULL,
"is_ads" text NOT NULL,
"share_url" text NOT NULL,
"statistics__comment_count" text NOT NULL,
"statistics__digg_count" text NOT NULL,
"statistics__play_count" text NOT NULL,
"statistics__share_count" text NOT NULL,
"video__play_addr__url_list__0" text NOT NULL
);
'''

    def open_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(self.connect_database())
        asyncio.get_event_loop().run_until_complete(self.create_table())

    def close_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(self.close_connect())

    def process_item(self, item, spider):
        place_holder = [f'${i+1}' for i in range(len(item.keys()))]
        self.sql_insert_item = f'''
INSERT INTO {self.table_name} ({', '.join(item.keys())}) VALUES
({', '.join(place_holder)})
ON CONFLICT DO NOTHING;
'''
        self.items_cache.append(tuple([str(v) for v in item.values()]))

        if len(self.items_cache) > self.cache_threshold:
            rows = copy.deepcopy(self.items_cache)
            self.items_cache.clear()

            # async insert.
            asyncio.get_event_loop().run_until_complete(
                self.flush_rows(rows))
        return item

    async def connect_database(self):
        """
        连接
        """
        self.conn = await asyncpg.connect(**postgre_configs)

    async def close_connect(self):
        if self.conn is not None:
            await self.conn.close()

    async def create_table(self):
        """
        创建表
        """
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.execute(self.sql_create_table)
        except Exception:
            await tr.rollback()
            raise
        finally:
            await tr.commit()

    async def flush_rows(self, rows):
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.executemany(self.sql_insert_item, rows)
        except Exception as e:
            await tr.rollback()
            raise
        finally:
            await tr.commit()
