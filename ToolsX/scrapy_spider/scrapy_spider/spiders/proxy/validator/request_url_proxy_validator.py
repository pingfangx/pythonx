import requests
import urllib3
from requests import ConnectTimeout, ReadTimeout, Response

from scrapy_spider.spiders.proxy.validator.base_proxy_validator import BaseProxyValidator


class RequestUrlProxyValidator(BaseProxyValidator):
    """通过请求地址来校验"""

    def __init__(self, url):
        self.url = url
        # 禁用 https 的警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        super().__init__()

    def get_url(self):
        return self.url

    def validate(self, proxy):
        ip, port, http_type = proxy['ip'], proxy['port'], proxy['http_type']
        proxy_url = f'{http_type}://{ip}:{port}'

        http_type = http_type.lower()
        proxies = {
            http_type: proxy_url
        }
        result = False
        response = None
        try:
            response = requests.get(self.get_url(), proxies=proxies, timeout=self.timeout, verify=False)
            if response.status_code == 200:
                try:
                    result = self.validate_response(proxy, response)
                except Exception as e:
                    # print(f'{proxy}-解析出错 {e}')
                    pass
            else:
                # print(f'{proxy}-失败，请求状态码{response.status_code}')
                pass
        except (ConnectTimeout, ConnectionError, ReadTimeout) as e:
            # print(f'{proxy}-连接超时 {e}')
            pass
        except Exception as e:
            # log.info(f'{proxy}-失败{type(e)}{e}')
            pass
        if response:
            response.close()
        return result

    def validate_response(self, proxy, response: Response) -> bool:
        """校验返回结果

        默认只要有返回结果就正确"""
        if response.text:
            return True
        else:
            return False
