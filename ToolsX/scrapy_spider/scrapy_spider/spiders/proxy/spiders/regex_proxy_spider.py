import re

from scrapy_spider.spiders.proxy.spiders.base_proxy_spider import BaseProxySpider
from scrapy_spider.spiders.proxy.spiders.parser.regex_proxy_parser import CoderBusyProxyParser
from scrapy_spider.spiders.proxy.spiders.parser.regex_proxy_parser import Data5uProxyParser
from scrapy_spider.spiders.proxy.spiders.parser.regex_proxy_parser import GoubanjiaProxyParser
from scrapy_spider.spiders.proxy.spiders.parser.regex_proxy_parser import RegexProxyParser


class BaseRegexProxySpider(BaseProxySpider):
    """通用的用正则就可以解析"""
    top_level_domain = 'com'
    cname = 'www'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = self.get_start_urls()

    def get_start_urls(self):
        """抓取地址"""
        return [f'http://{self.cname}.{self.name}.{self.top_level_domain}']

    def get_regex_pattern(self):
        """解析正则"""
        return None

    def get_proxy_parser(self):
        """获取解析器"""
        return RegexProxyParser(self.get_regex_pattern())

    def parse(self, response):
        proxy_parser = self.get_proxy_parser()
        proxy_list = proxy_parser.parse_proxy_list_from_response(response)

        available_proxy_list = self.filter_and_save_proxy_list(proxy_list)
        for proxy in available_proxy_list:
            yield proxy


class JiangxianliSpider(BaseRegexProxySpider):
    name = 'jiangxianli'
    cname = 'ip'


class IphaiSpider(BaseRegexProxySpider):
    name = 'iphai'


class CoderbusySpider(BaseRegexProxySpider):
    name = 'coderbusy'
    cname = 'proxy'

    def get_regex_pattern(self):
        # 以data-ip 开头，data-i 为端口密码，端口包在 >< 中
        return re.compile('data-ip.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?data-i.*?(\d+).*?>(\d{2,5})<.*?(http(s)?)',
                          re.IGNORECASE)

    def get_proxy_parser(self):
        return CoderBusyProxyParser(self.get_regex_pattern())


class GoubanjiaSpider(BaseRegexProxySpider):
    name = 'goubanjia'

    def get_regex_pattern(self):
        return re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\w+)-(\d{2,5}).*?(http(s)?)', re.IGNORECASE)

    def get_proxy_parser(self):
        return GoubanjiaProxyParser(self.get_regex_pattern())


class Ip3366Spider(BaseRegexProxySpider):
    name = 'ip3366'
    top_level_domain = 'net'


class _66ipSpider(BaseRegexProxySpider):
    name = '66ip'
    top_level_domain = 'cn'


class _89ipSpider(BaseRegexProxySpider):
    name = '89ip'
    top_level_domain = 'cn'


class swei360Spider(BaseRegexProxySpider):
    name = 'swei360'


class data5uSpider(BaseRegexProxySpider):
    name = 'data5u'

    def get_regex_pattern(self):
        # 端口加密
        return re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?port\s(\w+).*?>(\d{2,5})<.*?(http(s)?)',
                          re.IGNORECASE)

    def get_proxy_parser(self):
        return Data5uProxyParser(self.get_regex_pattern())


class kuaidailiSpider(BaseRegexProxySpider):
    name = 'kuaidaili'

    def get_start_urls(self):
        return [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/',
        ]


class XicidailiSpider(BaseRegexProxySpider):
    name = 'xicidaili'

    def get_start_urls(self):
        return [
            'http://www.xicidaili.com/nn/{page}',
            'http://www.xicidaili.com/nt/{page}',
            'http://www.xicidaili.com/wt/{page}',
            'http://www.xicidaili.com/wn/{page}',
        ]
