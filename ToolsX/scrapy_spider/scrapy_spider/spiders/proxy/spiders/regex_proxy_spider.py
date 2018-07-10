import re

from scrapy_spider.spiders.proxy.parser.regex_proxy_parser import CoderBusyProxyParser
from scrapy_spider.spiders.proxy.parser.regex_proxy_parser import Data5uProxyParser
from scrapy_spider.spiders.proxy.parser.regex_proxy_parser import GoubanjiaProxyParser
from scrapy_spider.spiders.proxy.parser.regex_proxy_parser import RegexProxyParser
from scrapy_spider.spiders.proxy.spiders.base_proxy_spider import BaseProxySpider


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


class XicidailiSpider(BaseRegexProxySpider):
    """还是有不少可用的"""
    ip_count = 24 / 400
    name = 'xicidaili'

    def get_start_urls(self):
        return [
            'http://www.xicidaili.com/nn/{page}',
            'http://www.xicidaili.com/nt/{page}',
            'http://www.xicidaili.com/wt/{page}',
            'http://www.xicidaili.com/wn/{page}',
        ]


class Data5uSpider(BaseRegexProxySpider):
    """有效率挺高的，因为是端口加密的"""
    ip_count = 13 / 20
    name = 'data5u'

    def get_regex_pattern(self):
        # 端口加密
        return re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?port\s(\w+).*?>(\d{2,5})<.*?(http(s)?)',
                          re.IGNORECASE)

    def get_proxy_parser(self):
        return Data5uProxyParser(self.get_regex_pattern())


class GoubanjiaSpider(BaseRegexProxySpider):
    """加密方式与 data5u 相同，还增加了样式来混淆"""
    ip_count = 6 / 20
    name = 'goubanjia'

    def get_regex_pattern(self):
        return re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\w+)-(\d{2,5}).*?(http(s)?)', re.IGNORECASE)

    def get_proxy_parser(self):
        return GoubanjiaProxyParser(self.get_regex_pattern())


class CoderbusySpider(BaseRegexProxySpider):
    """另一种端口加密方式"""
    ip_count = 5 / 50
    name = 'coderbusy'
    cname = 'proxy'

    def get_regex_pattern(self):
        # 以data-ip 开头，data-i 为端口密码，端口包在 >< 中
        return re.compile('data-ip.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?data-i.*?(\d+).*?>(\d{2,5})<.*?(http(s)?)',
                          re.IGNORECASE)

    def get_proxy_parser(self):
        return CoderBusyProxyParser(self.get_regex_pattern())


class Ip3366Spider(BaseRegexProxySpider):
    """每页只有一个，好在每页都有一个"""
    ip_count = 1 / 10
    name = 'ip3366'
    top_level_domain = 'net'
    max_page = 10

    def get_start_urls(self):
        return ['http://www.ip3366.net/?stype=1&page={page}', ]


class Six66ipSpider(BaseRegexProxySpider):
    """可分多个地区的 ip，而且有效率很高啊"""
    ip_count = 3 / 26
    name = '66ip'
    top_level_domain = 'cn'
    max_page = 34

    def get_start_urls(self):
        """页数用来代替地区"""
        return ['http://www.66ip.cn/areaindex_{page}/1.html', ]


# 以下已不可用
class KuaidailiSpider(BaseRegexProxySpider):
    """基本没有可用的了"""
    ip_count = 0
    name = 'kuaidaili'

    def get_start_urls(self):
        return [
            'https://www.kuaidaili.com/free/inha/{page}',
            'https://www.kuaidaili.com/free/intr/{page}',
        ]


class JiangxianliSpider(BaseRegexProxySpider):
    """没有可用的"""
    ip_count = 0
    name = 'jiangxianli'
    cname = 'ip'


class IphaiSpider(BaseRegexProxySpider):
    """503 打不开"""
    ip_count = 0
    name = 'iphai'


class Eight89ipSpider(BaseRegexProxySpider):
    """没一个可用"""
    ip_count = 0
    name = '89ip'
    top_level_domain = 'cn'
    max_page = 10

    def get_start_urls(self):
        return ['http://www.89ip.cn/index_{page}.html']


class Swei360Spider(BaseRegexProxySpider):
    """没有可用"""
    ip_count = 0
    name = 'swei360'
