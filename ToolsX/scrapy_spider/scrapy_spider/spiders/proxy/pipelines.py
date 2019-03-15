from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline, BasePostgreSQLPipelineTest
from scrapy_spider.spiders.proxy.items import ProxyItem


class ProxyPostgreSQLPipeline(BasePostgreSQLPipeline):
    """保存代理"""
    item = ProxyItem()


class ProxyPostgreSQLPipelineTest(BasePostgreSQLPipelineTest):
    pipeline = ProxyPostgreSQLPipeline()
    insert_item = ProxyItem(ip=1)
