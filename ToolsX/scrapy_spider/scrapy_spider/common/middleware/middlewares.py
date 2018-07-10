# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy_spider.common.ignore import douyin
from scrapy_spider.common.log import log
from scrapy_spider.common.middleware.agent_manager import AgentManager
from scrapy_spider.spiders.proxy.manager.proxy_manager import proxy_manager

from twisted.internet.error import ConnectionRefusedError


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
        proxy = request.meta['proxy']
        print(f'proxy is {proxy}')
        code, _ = douyin.parse_result(response.body.decode())
        if code == 1:
            proxy_manager.success(proxy)
        elif code == 2:
            proxy_manager.banned(proxy)
        else:
            proxy_manager.fail(proxy)
        return response

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        if isinstance(exception, ConnectionRefusedError):
            # 被拒绝
            print(f'proxy is {proxy}')
            proxy_manager.fail(proxy)
            return
        log.info("process_exception")
        log.info(f'proxy is {proxy}')
        log.info(type(exception))
        log.info(exception)


class RandomAgentDownloaderMiddleware(object):
    """随机 agent"""
    agent_manager = AgentManager()

    def process_request(self, request, spider):
        agent = self.agent_manager.random_agent()
        log.info(f'use random agent {agent}')
        request.headers.setdefault('User-Agent', agent)
