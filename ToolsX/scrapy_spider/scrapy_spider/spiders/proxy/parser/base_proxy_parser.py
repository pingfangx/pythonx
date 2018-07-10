import sys


class BaseProxyParser:
    """代理解析"""

    def parse_proxy_list(self, text):
        raise NotImplementedError(
            '{}.{} not implemented'.format(self.__class__.__name__, sys._getframe().f_code.co_name))
