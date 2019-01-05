import unittest

from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline
from scrapy_spider.spiders.weibo.items import WeiboVideoItem


class WeiboVideoPostgreSQLPipeline(BasePostgreSQLPipeline):
    item = WeiboVideoItem


class PipelineTest(unittest.TestCase):
    pipeline = WeiboVideoPostgreSQLPipeline()

    def test_create_table(self):
        self.pipeline.open_spider(None)
