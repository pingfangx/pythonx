# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import asyncio
import copy
import json
from scrapy_spider.items import AwemeItem
import asyncpg
from scrapy_spider.ignore.postgreconfig import postgre_configs
from scrapy_spider.items import DOUYIN_CREATE_TABLE_SQL
from scrapy_spider.items import DOUYIN_INSERT_SQL


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

    def open_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(self.connect_database())
        asyncio.get_event_loop().run_until_complete(self.create_table())

    def close_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(self.close_connect())

    def process_item(self, item, spider):
        sql = DOUYIN_INSERT_SQL.format(**item)
        asyncio.get_event_loop().run_until_complete(self.execute(sql))
        return item

    async def execute(self, sql):
        """执行 sql
        TODO 是否需要事务？如何优化
        """
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.execute(sql)
        except Exception:
            print('执行 sql 出错')
            print(sql)
            await tr.rollback()
            raise
        finally:
            await tr.commit()

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
            await self.conn.execute(DOUYIN_CREATE_TABLE_SQL)
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
