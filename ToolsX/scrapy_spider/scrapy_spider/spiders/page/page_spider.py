import os
import re
import urllib.parse

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
    cookies = {}

    def start_requests(self):
        for url in self.start_urls:
            url = self.generate_request_url(url)
            if url:
                print(f'load url {url} ' + (f'cookies={self.cookies}' if self.cookies else ''))
                yield scrapy.Request(url, cookies=self.cookies)

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
        url: str = self.remove_url_params(response.url)
        if not url.startswith(self.host):  # 可能因为跳转导致不在 host 下
            print(f'{url} 已不在 host 下 {self.host}')
            return ''
        file_path = url.replace(self.host, '')
        file_path = file_path.lstrip('/')  # 如果错误地以 / 开头，将其去除
        file_path = os.path.join(self.save_file_dir, file_path)
        file_path = page_utils.add_file_extension(file_path)
        print(f'url={url},path={file_path}')
        return file_path

    def remove_url_params(self, url: str):
        # 将 params query fragment 置空
        r = list(urllib.parse.urlparse(url))
        r[3] = ''
        r[4] = ''
        r[5] = ''
        url = urllib.parse.urlunparse(r)
        return url


class PageSpiderTest(BaseSpiderTest):
    spider = PageSpider


class AndroidDocPageSpider(PageSpider):
    name = 'android_doc_page'
    host = 'https://developer.android.google.cn/'
    cookies = {
        'django_language': 'zh_cn'
    }
    save_file_dir = r'D:\workspace\TranslatorX-other\AndroidSdkDocs\source\docs'
    start_urls = [
    ]

    def __init__(self, **kwargs):
        text = """
            """
        self.init_urls(text)
        self.valid_url = 0
        self.invalid_url = 0
        super().__init__(**kwargs)

    def generate_request_url(self, url):
        url = super().generate_request_url(url)
        # GFW
        url = url.replace('https://developer.android.com/', self.host)
        return url

    def init_urls(self, text):
        lines = text.split('\n')
        pattern = re.compile(r"\s*(.*?)\s*\((.*?)\)")
        lines_count = len(lines)
        count = 0
        inner = 0
        compat = 0
        for line in lines:
            if not line.strip():
                continue
            count += 1
            if '中' in line:
                inner += 1
                continue
            if 'AppCompat' in line:
                compat += 1
                continue
            match = re.search(pattern, line)
            if match:
                class_name = match.group(2) + "." + match.group(1)
                class_name = class_name.replace('.', "/")
                url = f"{self.host}reference/{class_name}.html"
                self.start_urls.append(url)
        print(f'共 {lines_count} 行'
              f'有效 {count} 行，可用地址 {len(self.start_urls)} 个，过滤内部类 {inner} 个，兼容类 {compat} 个')

    def parse(self, response):
        redirect_url_list = response.request.meta.get('redirect_urls')
        if redirect_url_list:
            url: str = response.url
            if url.endswith('classes.html') or url.endswith('reference'):
                self.invalid_url += 1
                print(f'无效地址 {self.invalid_url} 个')
                print(f'地址跳转 [{redirect_url_list[0]}] -> [{url}]')
                return
            else:
                print(f'地址跳转 [{redirect_url_list[0]}] -> [{url}]')
        self.valid_url += 1
        print(f'有效地址 {self.valid_url} 个')
        return super().parse(response)


class AndroidDocPageSpiderTest(BaseSpiderTest):
    spider = AndroidDocPageSpider
