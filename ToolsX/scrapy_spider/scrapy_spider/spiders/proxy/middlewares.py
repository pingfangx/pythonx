from scrapy_spider.common.middleware.middlewares import RandomProxyDownloaderMiddleware, ErrorResponse
from scrapy_spider.spiders.douyin import douyin_spider
from scrapy_spider.spiders.douyin.ignore import douyin
from scrapy_spider.spiders.proxy.items import ProxyItem
from scrapy_spider.spiders.proxy.manager.proxy_manager import proxy_manager


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

        if isinstance(response, ErrorResponse):
            proxy_manager.fail(proxy)
            return self.on_request_error(request, response, spider)
        code, _ = douyin.parse_result(response.body.decode())
        if code == 1:
            proxy_manager.success(proxy)
        elif code == 2:
            proxy_manager.banned(proxy)
            if douyin_spider.ANONYMOUS:
                # 匿名则忽略并继续 ，不匿名返回处理
                return self.on_request_error(request, response, spider)
            else:
                return response
        else:
            proxy_manager.fail(proxy)
            return self.on_request_error(request, response, spider)
        return response
