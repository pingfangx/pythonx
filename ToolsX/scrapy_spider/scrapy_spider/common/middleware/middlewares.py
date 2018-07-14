# -*- coding: utf-8 -*-

from scrapy.exceptions import IgnoreRequest
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http import Response
from scrapy_spider.common.ignore import douyin
from scrapy_spider.common.log import log
from scrapy_spider.common.middleware.agent_manager import AgentManager
from scrapy_spider.spiders.douyin import douyin_spider
from scrapy_spider.spiders.proxy.items import ProxyItem
from scrapy_spider.spiders.proxy.manager.proxy_manager import proxy_manager
from twisted.internet import error
from twisted.web._newclient import ResponseNeverReceived


class RandomProxyDownloaderMiddleware(object):
    """随机代理"""

    def process_request(self, request, spider):
        proxy = proxy_manager.get()
        log.info(f'use random proxy {proxy}')
        request.meta["proxy"] = str(proxy)


class DouyinRandomProxyDownloaderMiddleware(RandomProxyDownloaderMiddleware):
    """抖音的随机代理中间件"""

    def process_response(self, request, response, spider):
        """
        要考虑两种情况，一是被封，二是ip 失效
        :param request:
        :param response:
        :param spider:
        :return:
        """
        proxy_str = request.meta['proxy']
        proxy = ProxyItem.parse(proxy_str)
        # 持有的是方法，只有一个实例，所以并发时 self.proxy 应该是不准确的，需从 request 获取
        code, _ = douyin.parse_result(response.body.decode())
        if code == 1:
            proxy_manager.success(proxy)
        elif code == 2:
            proxy_manager.banned(proxy)
            if douyin_spider.ANONYMOUS:
                # 匿名则忽略并继续 ，不匿名返回处理
                raise IgnoreRequest()
            else:
                return response
        else:
            proxy_manager.fail(proxy)
            raise IgnoreRequest()
        return response

    def process_exception(self, request, exception, spider):
        proxy_str = request.meta['proxy']
        proxy = ProxyItem.parse(proxy_str)
        if isinstance(exception, IgnoreRequest):
            # 已忽略
            return self.get_error_response(exception)
        else:
            # 检查是否是已知的错误，如果是未知错误，可能需要记录处理
            fail_exception_list = [
                error.ConnectError,
                error.ConnectionRefusedError,
                error.TCPTimedOutError,
                error.TimeoutError,  # 超过设定的 timeout
                ResponseNeverReceived,
            ]
            for e in fail_exception_list:
                if isinstance(exception, e):
                    # 被拒绝
                    # 此处不调用 fail，返回 response 之后会在 process_response 中处
                    # proxy_manager.fail(proxy)
                    return self.get_error_response(exception)
        log.error("process_exception")
        log.error(f'proxy is {proxy}')
        log.error(type(exception))
        log.error(exception)

    def get_error_response(self, exception=None):
        """用于 process_exception 方法
        返回 None 异常还会继续被片理
        返回 Response 会调用 parse 方法"""
        print(f'已拦截异常 {type(exception)}')
        return Response('', body=b'error')


class RandomAgentDownloaderMiddleware(object):
    """随机 agent"""
    agent_manager = AgentManager()

    def process_request(self, request, spider):
        agent = self.agent_manager.random_agent()
        # log.info(f'use random agent {agent}')
        request.headers.setdefault('User-Agent', agent)
