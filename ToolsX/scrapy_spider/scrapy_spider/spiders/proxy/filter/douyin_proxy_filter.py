from scrapy_spider.spiders.proxy.filter.base_proxy_filter import BaseProxyFilter
from scrapy_spider.spiders.proxy.validator.douyin_proxy_validator import DouyinProxyValidator
from scrapy_spider.spiders.proxy.validator.telnet_proxy_validator import TelnetProxyValidator


class DouyinProxyFilter(BaseProxyFilter):
    """抖音代理过滤"""

    def __init__(self, proxy_list):
        # 先 telnet 校验,再 douyin 校验
        self.douyin_proxy_validator = DouyinProxyValidator()
        validator_list = [
            TelnetProxyValidator(),
            self.douyin_proxy_validator,
        ]
        super().__init__(proxy_list, validator_list)

    def after_filter(self):
        self.douyin_proxy_validator.save_items()
