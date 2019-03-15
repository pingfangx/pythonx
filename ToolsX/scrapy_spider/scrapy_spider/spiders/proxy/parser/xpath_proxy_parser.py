from lxml import etree

from scrapy_spider.common.log import log
from scrapy_spider.spiders.proxy.items import ProxyItem
from scrapy_spider.spiders.proxy.parser.base_proxy_parser import BaseProxyParser


class XpathProxyParser(BaseProxyParser):
    """代理解析，用 xpath 很低效，不如正则方便"""

    def __init__(self, xpath_element_list=None, xpath_element_formatter=None, xpath_element_dict=None,
                 parse_element_list_method=None, parse_element_method=None, parse_proxy_extra_method=None):
        self.xpath_element_list = xpath_element_list
        """解析元素列表的 xpath"""

        self.xpath_element_formatter = xpath_element_formatter
        """解析元素的 xpath 的格式化串"""

        self.xpath_element_dict = xpath_element_dict
        """解析元素的 xpath 字典，用于格式化"""

        self.parse_element_list_method = parse_element_list_method
        """解析元素列表的方法"""
        if self.parse_element_list_method is None:
            self.parse_element_list_method = self.parse_element_list_from_text

        self.parse_proxy_method = parse_element_method
        """解析代理的方法"""
        if self.parse_proxy_method is None:
            self.parse_proxy_method = self.parse_proxy_from_element

        self.parse_proxy_extra_method = parse_proxy_extra_method
        """解析出代理后额外的处理方法"""

    def parse_proxy_list_from_response(self, response):
        """解析代理"""
        return self.parse_proxy_list(response.text)

    def parse_proxy_list(self, text):
        """解析代理"""
        element_list = self.parse_element_list_method(text, self.xpath_element_list)
        if not element_list:
            return []

        proxy_list = []
        for element in element_list:
            try:
                proxy_item = self.parse_proxy_method(element, self.xpath_element_formatter, self.xpath_element_dict)
                if self.parse_proxy_extra_method:
                    proxy_item = self.parse_proxy_extra_method(element, proxy_item)
                proxy_list.append(proxy_item)
            except Exception as e:
                log.error(e)
        return proxy_list

    @staticmethod
    def parse_element_list_from_text(text, xpath_element_list):
        """解析出元素列表"""
        if not xpath_element_list:
            return None

        selector = etree.HTML(text)
        element_list = selector.xpath(xpath_element_list)
        return element_list

    @staticmethod
    def parse_proxy_from_element(element, element_xpath_formatter=None, element_xpath_dict=None):
        """从元素中解析代理"""
        proxy_item = ProxyItem()
        if element_xpath_formatter and element_xpath_dict:
            for k, v in element_xpath_dict.items():
                if '-' in v:
                    v, xpath = v.split('-')
                else:
                    xpath = element_xpath_formatter
                xpath = xpath % v
                proxy_item[k] = element.xpath(xpath)[0]
        return proxy_item


class CoderBusyXpathProxyParser(XpathProxyParser):
    def __init__(self):
        xpath_element_list = '//table/tbody/tr'
        super().__init__(xpath_element_list, parse_proxy_extra_method=self.decrypt)

    def decrypt(self, element, proxy_item):
        """解密"""
        ip_port_td = element.xpath('./td[3]')[0]
        ip = ip_port_td.attrib['data-ip']

        port_password = ip_port_td.attrib['data-i']
        port_password = int(port_password)
        for i in ip.split('.'):
            port_password -= int(i)
        port = str(port_password)

        if len(element.xpath('./td[9]/i')) > 0:
            # 有 i 表示是 https
            http_type = 'https'
        else:
            http_type = 'http'
        proxy_item['ip'] = ip
        proxy_item['port'] = port
        proxy_item['http_type'] = http_type
        return proxy_item
