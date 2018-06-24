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


class RandomAgentDownloaderMiddleware(object):
    """随机 agent"""
    agent_manager = AgentManager()

    def process_request(self, request, spider):
        agent = self.agent_manager.random_agent()
        log.info(f'use random agent {agent}')
        request.headers.setdefault('User-Agent', agent)
