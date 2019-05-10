import os

import scrapy
from base_spider_test import BaseSpiderTest
from scrapy_spider.spiders.page import page_utils
from scrapy_spider.spiders.page.items import PageItem


class PageSpider(scrapy.Spider):
    """网页爬虫，爬取后用于翻译"""

    name = 'page'
    start_urls = [
        '',
    ]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spider.spiders.page.middlewares.PageMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.page.pipelines.PagePipelines': 300,
        },
    }

    host = ''
    """host，地址不全时自动拼接"""
    save_file_dir = ''
    """保存文件的目录"""

    def start_requests(self):
        for url in self.start_urls:
            url = self.generate_request_url(url)
            if url:
                print(f'load url {url}')
                yield scrapy.Request(url)

    def generate_request_url(self, url):
        """生成请求地址"""
        if not url.startswith('http'):
            url = os.path.join(self.host, url)
        return url

    def parse(self, response):
        data = {
            'text': response.text,
            'path': self.get_file_path(response)
        }
        yield PageItem(data)

    def get_file_path(self, response):
        """获取文件路径"""
        url: str = response.url
        file_path = url.replace(self.host, '')
        file_path = os.path.join(self.save_file_dir, file_path)
        file_path = page_utils.add_file_extension(file_path)
        return file_path


class PageSpiderTest(BaseSpiderTest):
    spider = PageSpider


class AndroidDocPageSpider(PageSpider):
    name = 'android_doc_page'
    host = 'https://developer.android.google.cn/'
    save_file_dir = r'D:\workspace\TranslatorX-other\AndroidSdkDocs\source\docs'
    start_urls = [
        '',
    ]

    def generate_request_url(self, url):
        url = super().generate_request_url(url)
        # GFW
        url = url.replace('https://developer.android.com/', self.host)
        return url


class AndroidDocPageSpiderTest(BaseSpiderTest):
    spider = AndroidDocPageSpider
