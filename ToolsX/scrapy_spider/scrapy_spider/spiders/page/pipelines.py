from scrapy_spider.spiders.page import page_utils


class PagePipelines:
    """保存文件"""

    def process_item(self, item, spider):
        page_utils.save_file(item['path'], item['text'])
