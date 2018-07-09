# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy_spider.common.log import log
from scrapy_spider.common.middleware.agent_manager import AgentManager
from scrapy_spider.common.middleware.proxy_manager import ProxyManager


class RandomProxyDownloaderMiddleware(object):
    """随机代理"""
    proxy_manager = ProxyManager()

    def process_request(self, request, spider):
        proxy = self.proxy_manager.random_proxy()
        log.info(f'use random proxy {proxy}')
        request.meta["proxy"] = proxy

    def process_response(self, request, response, spider):
        """
        要考虑两种情况，一是被封，二是ip 失效
        :param request:
        :param response:
        :param spider:
        :return:
        """
        print("process_response")
        print(response)
        proxy = request.meta['proxy']
        print(f'proxy is {proxy}')
        return response

    def process_exception(self, request, exception, spider):
        print("process_exception")
        print(exception)
        pass


class RandomAgentDownloaderMiddleware(object):
    """随机 agent"""
    agent_manager = AgentManager()

    def process_request(self, request, spider):
        agent = self.agent_manager.random_agent()
        log.info(f'use random agent {agent}')
        request.headers.setdefault('User-Agent', agent)
