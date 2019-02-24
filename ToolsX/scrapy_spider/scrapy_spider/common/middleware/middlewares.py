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
        """处理请求"""
        proxy = proxy_manager.get()
        log.info(f'use random proxy {proxy}')
        request.meta["proxy"] = str(proxy)

    def process_response(self, request, response, spider):
        """
        处理回复
        如果是 ErrorResponse 则记录失败
        否则判断并记录成功

        如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理。
        如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样。
        如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。
        """
        proxy_str = request.meta['proxy']
        proxy = ProxyItem.parse(proxy_str)
        if isinstance(response, ErrorResponse):
            # 请求失败
            proxy_manager.fail(proxy)
            print('请求失败，记录失败，重新请求')
            return self.on_request_error(request, response, spider)
        elif not self.is_success_response(response):
            # 回复解析失败
            proxy_manager.fail(proxy)
            print('回复解析失败，记录失败，重新请求')
            return self.on_request_error(request, response, spider)
        else:
            # 回复成功
            print('回复解析成功，记录成功')
            proxy_manager.success(proxy)
        return response

    def on_request_error(self, request, response, spider):
        """
        当请求错误时
        :return: 如果返回 IgnoreRequest 这个请求会被忽略，但是实际没有请求成功
        下一次请求时，再次执行相同请求，会被重复过滤
        所以返回新设置代理的请求，但是如果从 process_exception 而来，好像会报错需要继承 BaseException，待重现
        """
        self.process_request(request, spider)
        raise request

    def is_success_response(self, response):
        """是否是成功的请求，可由子类重写"""
        return True

    def process_exception(self, request, exception, spider):
        """
        处理异常
        如果超时了，则抛出一个 ErrorResponse，交给 process_response 处理

        如果其返回 None ，Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception() 方法，直到所有中间件都被调用完毕，则调用默认的异常处理。
        如果其返回一个 Response 对象，则已安装的中间件链的 process_response() 方法被调用。Scrapy将不会调用任何其他中间件的 process_exception() 方法。
        如果其返回一个 Request 对象， 则返回的request将会被重新调用下载。这将停止中间件的 process_exception() 方法执行，就如返回一个response的那样。
        """
        proxy_str = request.meta['proxy']
        proxy = ProxyItem.parse(proxy_str)
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
        return ErrorResponse('')


class ErrorResponse(Response):
    """错误的回复"""


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
