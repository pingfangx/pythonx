import asyncio

import asyncpg
from scrapy import cmdline
from scrapy_spider.ignore.postgreconfig import postgre_configs
from scrapy_spider.items import AwemeItem
from scrapy_spider.items import DOUYIN_CREATE_TABLE_SQL
from scrapy_spider.items import DOUYIN_INSERT_SQL
from scrapy_spider.pipelines import PostgreSQLPipeline


class Test:

    @staticmethod
    def run_spider_to_json():
        spider = "douyin"
        args = "-o items.json"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())

    @staticmethod
    def run_spider():
        """运行爬虫"""
        spider = "douyin"
        args = ""
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())

    @staticmethod
    def connect_db():
        """连接数据库"""
        conn = asyncpg.connect(**postgre_configs)
        conn.close()

    def create_table(self):
        """建表"""
        pipe = PostgreSQLPipeline()
        pipe.open_spider('')

    @staticmethod
    async def execute(sql):
        print("执行", sql)
        conn = await asyncpg.connect(**postgre_configs)
        await conn.execute(sql)
        await conn.close()

    @staticmethod
    def insert_item():
        item = AwemeItem(aweme_id='1', desc_="test")
        pipe = PostgreSQLPipeline()
        pipe.open_spider('')
        pipe.process_item(item, None)

    def test(self):
        # print(DOUYIN_CREATE_TABLE_SQL)
        # self.create_table()
        # print(DOUYIN_INSERT_SQL)
        # self.insert_item()
        self.run_spider()
        pass


if __name__ == '__main__':
    Test().test()
