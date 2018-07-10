class BaseProxyValidator:
    """代理校验"""

    def __init__(self, timeout=3):
        """
        超时
        :param timeout:
        """
        self.timeout = timeout

    def validate(self, proxy):
        """校验"""
        return self.validate_proxy(proxy['http_type'].lower(), proxy['ip'], proxy['port'])

    def validate_proxy(self, http_type, ip, port):
        """
        校验代理
        :param http_type: http 或 https
        :param ip: ip
        :param port: 端口
        :return:
        """
        return False
