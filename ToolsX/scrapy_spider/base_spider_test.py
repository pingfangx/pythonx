import unittest

from scrapy import cmdline


class BaseSpiderTest(unittest.TestCase):
    """爬虫测试，因为设置 SPIDER_MODULES 所以需位于正确的目录"""

    spider = None
    """要测试的爬虫，需要有 name 属性"""

    def test_run_spider(self):
        """运行爬虫"""
        args = f'--set SPIDER_MODULES={self.get_class_relative_package(self.spider)}'
        cmd = f'scrapy crawl {self.spider.name} {args}'
        cmdline.execute(cmd.split())

    @staticmethod
    def get_spider_modules(spider_name):
        """获取默认的爬虫模块

        按标准命名，取 scrapy_spider.spiders. 加上爬虫名
        """
        return f'scrapy_spider.spiders.{spider_name}'

    @staticmethod
    def get_class_relative_package(clazz):
        """根据类获取相对于当前文件的包名，用于 SPIDER_MODULES"""
        import os
        import sys
        module_name = clazz.__module__
        module_info = sys.modules[module_name]
        module_file = module_info.__file__
        module_dir = os.path.dirname(module_file)
        package_path = os.path.relpath(module_dir, __file__)
        package_name = package_path.replace(os.sep, '.').lstrip('.')
        return package_name
