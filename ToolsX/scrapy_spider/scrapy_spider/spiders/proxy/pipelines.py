import unittest

from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline
from scrapy_spider.spiders.proxy.items import ProxyItem


class ProxyPostgreSQLPipeline(BasePostgreSQLPipeline):
    """保存代理"""
    item = ProxyItem


class ProxyPostgreSQLPipelineTest(unittest.TestCase):
    def test_create_table(self):
        pipeline = ProxyPostgreSQLPipeline()
        pipeline.open_spider(None)

    def test_insert(self):
        pipeline = ProxyPostgreSQLPipeline()
        pipeline.open_spider(None)
        pipeline.process_item(ProxyItem(ip=1), None)
