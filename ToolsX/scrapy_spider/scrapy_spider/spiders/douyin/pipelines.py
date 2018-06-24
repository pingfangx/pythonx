import unittest

from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline
from scrapy_spider.spiders.douyin.items import DouyinItem


class DouyinPostgreSQLPipeline(BasePostgreSQLPipeline):
    """保存代理"""
    item = DouyinItem


class DouyinPostgreSQLPipelineTest(unittest.TestCase):
    def test_create_table(self):
        pipeline = DouyinPostgreSQLPipeline()
        pipeline.open_spider(None)

    def test_insert(self):
        pipeline = DouyinPostgreSQLPipeline()
        pipeline.open_spider(None)
        pipeline.process_item(DouyinItem(aweme_id=1), None)
