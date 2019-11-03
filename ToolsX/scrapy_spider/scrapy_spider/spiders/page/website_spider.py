import os
from urllib.parse import urljoin

import scrapy
from base_spider_test import BaseSpiderTest
from lxml import etree
from lxml.etree import _Element
from scrapy_spider.common.statistic.remaining_time_tatistics import RemainingTimeStatistics
from scrapy_spider.spiders.page.items import PageItem
from scrapy_spider.spiders.page.page_spider import PageSpider


def log_d(msg):
    # print(msg)
    pass


def log_i(msg):
    print(msg)


class WebsiteSpider(PageSpider):
    """爬取整站"""
    name = 'website'

    save_file_dir = ''
    """保存目录"""
    host = ''
    """仅爬取该域名下的网址"""
    start_urls = [
        '',
    ]
    """爬取的地址"""

    website_mode = True
    """
    网站模式，为 True 时解析页面中的链接
    为 False 只爬取单个页面
    """

    scrap_urls = {}
    """记录所有爬取的地址，
    key 为地址 
    value 0 为新添加，1 为已爬取取"""

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_spider.spiders.page.middlewares.WebsiteMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.page.pipelines.PagePipelines': 300,
        },
    }

    statistics = RemainingTimeStatistics()

    def parse(self, response):
        selector: _Element = etree.HTML(bytes(bytearray(response.text, encoding='utf-8')))
        if selector is None:
            log_i('selector 为空')
            return

        current_url = self.remove_url_params(response.url)
        log_i(f'开始解析数据 {current_url}')
        # 保存数据
        file_path = self.get_file_path(response)
        if file_path:
            data = {
                'text': response.text,
                'path': file_path
            }
            yield PageItem(data)
        if not self.website_mode:
            return

        # 记为已爬取
        self.scrap_urls[current_url] = 1

        a_list = selector.xpath('//a')

        link_host = 0
        for a in a_list:
            if 'href' not in a.attrib:
                continue
            link: str = a.attrib['href']
            if not link:
                continue
            link = self.remove_url_params(link)
            # 后缀
            suffix = os.path.splitext(link)[1]
            if not self.check_suffix(suffix):
                log_d(f'地址 {link} 后缀 {suffix} 不允许')
                continue
            # 拼接
            link = urljoin(current_url, link)
            # host
            if not link.startswith(self.host) or link == self.host:
                # log_d(f'地址 {link} 不在 host 下')
                continue
            # 有效
            if not (link in self.scrap_urls.keys()):
                log_i(f'新增地址 {link}')
                link_host += 1
                self.scrap_urls[link] = 0
            yield scrapy.Request(link, cookies=self.cookies)
        all_pages = len(self.scrap_urls)
        scrap_pages = len(list(filter(lambda x: x == 1, self.scrap_urls.values())))
        log_i(f'本页新增链接 {link_host} 个，总计 {scrap_pages}/{all_pages}')
        self.statistics.total = all_pages
        self.statistics.count(scrap_pages)

    @staticmethod
    def check_suffix(suffix: str) -> bool:
        """检查后缀"""
        # 只接收 html 的
        return suffix == '' or suffix == '.html'


class JavaTutorialSpider(WebsiteSpider):
    name = 'java_tutorial'
    save_file_dir = r'D:\file\java-tutorials'
    host = 'https://pingfangx.github.io/java-tutorials/'
    start_urls = [
        'https://pingfangx.github.io/java-tutorials/index.html',
    ]


class JavaTutorialSpiderTest(BaseSpiderTest):
    spider = JavaTutorialSpider


class AndroidGuideSpider(WebsiteSpider):
    name = 'android_guide'
    cookies = {
        'django_language': 'zh_cn'
    }
    save_file_dir = r'F:\android-sdk\docs-cn\guide'
    host = 'https://developer.android.google.cn/guide'
    website_mode = False
    start_urls = [
        'https://developer.android.google.cn/guide/index.html',
    ]


class _AndroidGuideSpider(BaseSpiderTest):
    spider = AndroidGuideSpider
