import time
import unittest

from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.spider import iter_spider_classes
from scrapy_spider.common.log import log
from scrapy_spider.spiders.proxy.manager.proxy_manager import proxy_manager
from scrapy_spider.spiders.proxy.spiders import regex_proxy_spider
from twisted.internet import reactor, defer


def test_spider(spider, modules):
    """
    测试爬虫
    :param spider: 爬虫名，即 name 指定的名字
    :param modules: 模块目录
    """
    args = f'--set SPIDER_MODULES={modules}'
    cmd = f'scrapy crawl {spider} {args}'
    cmdline.execute(cmd.split())


class TestDouyinSpider(unittest.TestCase):
    """抖音爬虫"""

    def test_run_spider(self):
        """运行抖音爬虫"""
        spider = "douyin"
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.douyin"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())


class TestWeiboVideoSpider(unittest.TestCase):
    """微博视频"""

    def test_weibo_video_spider(self):
        spider = "weibo_video"
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.weibo"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())


class TestProxySpider(unittest.TestCase):
    """爬取代理的爬虫"""

    def test_xicidaili_spider(self):
        self.test_proxy_spider('xicidaili')

    def test_data5u_spider(self):
        self.test_proxy_spider('data5u')

    def test_goubanjia_spider(self):
        self.test_proxy_spider('goubanjia')

    def test_coderbusy_spider(self):
        self.test_proxy_spider('coderbusy')

    def test_ip3366_spider(self):
        self.test_proxy_spider('ip3366')

    def test_66ip_spider(self):
        self.test_proxy_spider('66ip')

    # 以下已不可用
    def test_kuaidaili_spider(self):
        self.test_proxy_spider('kuaidaili')

    def test_jiangxianli_spider(self):
        self.test_proxy_spider('jiangxianli')

    def test_iphai_spider(self):
        self.test_proxy_spider('iphai')

    def test_89ip_spider(self):
        self.test_proxy_spider('89ip')

    def test_swei360_spider(self):
        self.test_proxy_spider('swei360')

    def test_coderbusy_regex_spider(self):
        self.test_proxy_spider('coderbusy_regex')

    # 测试方法
    def test_proxy_spider(self, spider):
        """运行代理爬虫"""
        args = "--set SPIDER_MODULES=scrapy_spider.spiders.proxy.spiders"
        cmd = "scrapy crawl %s %s" % (spider, args)
        cmdline.execute(cmd.split())


class TestAllProxySpider(unittest.TestCase):
    """所有的代理爬虫"""

    @defer.inlineCallbacks
    def crawl_in_loop(self, runner):
        """在循环中爬取"""
        # 遍历取出 spider
        spider_list = []
        for spider_class in iter_spider_classes(regex_proxy_spider):
            ip_count = getattr(spider_class, 'ip_count', 0)
            if ip_count > 0:
                spider_list.append(spider_class)
        loop_times = 0
        loop_end_count = 0
        all_loop_proxy_count = 0
        """整个循环中爬取的代理总数"""
        # 无限循环
        while loop_times >= 0:
            loop_times += 1

            available_count = proxy_manager.available_count()
            while available_count > 100:
                print(f'有效 ip {available_count} 个，休息 10 分钟')
                time.sleep(60 * 10)
                available_count = proxy_manager.available_count()

            # 开始时的数量
            if loop_end_count == 0:
                # 首次获取
                loop_start_count = proxy_manager.count()
            else:
                # 取循环结束时的获取
                loop_start_count = loop_end_count
            log.info(f'第 {loop_times} 轮爬取开始，当前 ip 共 {available_count}/{loop_start_count} 个')

            # 爬取

            spider_end_count = 0
            for i in range(len(spider_list)):
                spider = spider_list[i]
                if spider_end_count == 0:
                    spider_start_count = loop_start_count
                else:
                    spider_start_count = spider_end_count
                log.info(
                    f'第 {loop_times} 轮,第 {i + 1}/{len(spider_list)} 个爬虫 {spider.name} 开始爬取,'
                    f'当前 ip 共 {spider_start_count} 个')

                spider = spider_list[i]
                try:
                    yield runner.crawl(spider)
                except SystemExit:
                    pass
                sleep_time = 10
                spider_end_count = proxy_manager.count()
                spider_crawled_count = spider_end_count - spider_start_count
                loop_crawled_count = spider_end_count - loop_start_count
                # 单次循环爬取到的数量
                all_loop_proxy_count += loop_crawled_count
                divider = '-' * 10
                log.info(
                    f'{divider}第 {loop_times} 轮,第 {i + 1}/{len(spider_list)} 个爬虫 {spider.name} 爬取结束,'
                    f'共爬取到 {spider_crawled_count}/{loop_crawled_count}/{all_loop_proxy_count} 个代理{divider}')
                log.info(f'等待执行下一爬虫,sleep {sleep_time}')
                log.info(f'当前有效代理共 {proxy_manager.available_count()} 个')
                time.sleep(sleep_time)

            # 结束时的数量
            loop_end_count = proxy_manager.count()
            # 延时下一轮
            sleep_time = 60
            log.info(f'本轮共爬到 {loop_end_count - loop_start_count}/{loop_end_count} 个代理，等待下一轮,sleep {sleep_time}')
            log.info(f'当前有效代理共 {proxy_manager.available_count()} 个')
            time.sleep(sleep_time)
        reactor.stop()

    def test_proxy_spider_list(self):
        """多个代理爬虫"""
        configure_logging()
        runner = CrawlerRunner(get_project_settings())
        self.crawl_in_loop(runner)
        reactor.run()
