import re

from scrapy_spider.spiders.proxy.items import ProxyItem
from scrapy_spider.spiders.proxy.parser.base_proxy_parser import BaseProxyParser


class RegexProxyParser(BaseProxyParser):
    """代理解析"""

    def __init__(self, pattern=None):

        self.pattern = pattern
        """正则"""
        if self.pattern is None:
            self.pattern = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,5}).*?(http(s)?)', re.IGNORECASE)

    def parse_proxy_list_from_response(self, response):
        return self.parse_proxy_list(response.text)

    def parse_proxy_list(self, text):
        """解析代理"""
        # 将回车替换，方便正则查找
        text = text.replace('\n', '')
        all_match = re.findall(self.pattern, text)

        proxy_list = []
        if all_match:
            for match in all_match:
                ip, port, http_type = self.parse_proxy_from_match(match)
                if ip not in [proxy['ip'] for proxy in proxy_list]:
                    proxy_item = ProxyItem()
                    proxy_item['ip'] = ip
                    proxy_item['port'] = port
                    proxy_item['http_type'] = http_type
                    proxy_list.append(proxy_item)
        return proxy_list

    def parse_proxy_from_match(self, match):
        """从匹配结果中解析出代理"""
        http_type = None
        if len(match) >= 3:
            ip, port, http_type = match[0:3]
        else:
            ip, port = match[0:2]
        if not http_type:
            http_type = 'http'
        return ip, port, http_type


class Data5uProxyParser(RegexProxyParser):
    """
    端口加密了，搜了一下，找到
    https://github.com/ChansEbm/goubanjia/blob/master/spider/goubanjia.py
    感谢
    """

    def parse_proxy_from_match(self, match):
        ip, port_password, port, http_type = match[0:4]
        port = self.parse_port(port_password)
        return ip, port, http_type

    @staticmethod
    def parse_port(port_password):
        port_key = 'ABCDEFGHIZ'
        # 拼接位置
        port_list = [str(port_key.find(c)) for c in port_password]
        # 拼出端口
        port = "".join(port_list)
        # 右移 3 位
        return int(port) >> 0x3


class GoubanjiaProxyParser(Data5uProxyParser):
    """
    https://github.com/ChansEbm/goubanjia/blob/master/spider/goubanjia.py
    除了处理数据，还需要端口解密
    """

    def parse_proxy_list(self, text):
        # 处理 text
        # 为 none 的去掉
        text = re.sub('<p.*?none.*?>.*?</p>', '', text)
        # 保留密码
        text = re.sub('<span\sclass="port\s(\w+)">(\d+)</span>', '\\1-\\2', text)
        # 过滤样式，单个数字，点，或组合，或为空，都过滤掉
        text = re.sub('<(span|div).*?>(\d+|\.|\d+\.|\.\d+|)</\\1>', '\\2', text)
        return super().parse_proxy_list(text)


class CoderBusyProxyParser(RegexProxyParser):
    """
    端口加密了，找到了加密 js，但是看不太懂
    搜到
    [码农代理免费代理ip端口字段js加密破解](https://www.cnblogs.com/cc11001100/p/8606160.html)
    感谢
    """

    def parse_proxy_from_match(self, match):
        ip, port_password, port, http_type = match[0:4]
        port_password = int(port_password)
        for i in ip.split('.'):
            port_password -= int(i)
        port = str(port_password)
        return ip, port, http_type
