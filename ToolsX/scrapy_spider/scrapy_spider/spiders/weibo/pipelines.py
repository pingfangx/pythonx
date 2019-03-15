from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline, BasePostgreSQLPipelineTest
from scrapy_spider.spiders.weibo.items import WeiboVideoItem


class WeiboVideoPostgreSQLPipeline(BasePostgreSQLPipeline):
    item = WeiboVideoItem()


class PipelineTest(BasePostgreSQLPipelineTest):
    pipeline = WeiboVideoPostgreSQLPipeline()
