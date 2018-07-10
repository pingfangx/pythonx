import telnetlib

from scrapy_spider.spiders.proxy.validator.base_proxy_validator import BaseProxyValidator


class TelnetProxyValidator(BaseProxyValidator):
    """使用 telnet 校验
    好像无法校验 https
    """

    def validate_proxy(self, http_type, ip, port):
        try:
            telnetlib.Telnet(ip, port=port, timeout=self.timeout)
            return True
        except:
            return False
