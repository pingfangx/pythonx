from scrapy_spider.common.pipeline.postgresql_pipelines import BasePostgreSQLPipeline, BasePostgreSQLPipelineTest
from scrapy_spider.spiders.douyin.items import DouyinItem


class DouyinPostgreSQLPipeline(BasePostgreSQLPipeline):
    """保存代理"""
    item = DouyinItem()


class DouyinPostgreSQLPipelineTest(BasePostgreSQLPipelineTest):
    pipeline = DouyinPostgreSQLPipeline()
    insert_item = DouyinItem(aweme_id=1)
