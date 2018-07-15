import datetime
import unittest

from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLHelper
from scrapy_spider.spiders.douyin.items import DouyinItem


class DouyinManager:
    """数据管理"""

    def __init__(self):
        item = DouyinItem()
        self.table_name = item.get_table_name()
        self.helper = PostgreSQLHelper(item)

    def list_items_by_digg_count(self, days_before_today=1):
        """按点赞次数
        :param days_before_today: 多少天以前
        """

        # 计算时间
        now = datetime.datetime.today()
        if days_before_today == 0:
            today_zero = now.timestamp()
            today_before = 0
        else:
            today_zero = datetime.datetime(now.year, now.month, now.day)
            today_before = today_zero - datetime.timedelta(days=days_before_today)
        sql = f"""
        SELECT author__nickname,desc_,statistics__digg_count,share_url,create_time FROM {self.table_name}
        WHERE create_time >= {today_before.timestamp()} AND create_time < {today_zero.timestamp()}
        ORDER BY statistics__digg_count DESC
        LIMIT 10 
        """
        self.fetch(sql)

    def fetch(self, sql):
        print(sql)
        result = self.helper.fetch(sql)
        if not result:
            print('没有查询结果')
        else:
            length = len(result)
            for i in range(length):
                item = DouyinItem(**result[i])
                # 时间需要更新一下
                item['create_time'] = result[i]['create_time']
                self.print_item(item, f'{i+1}/{length} ')

    def print_item(self, item: DouyinItem, pre=''):
        create_time = datetime.datetime.fromtimestamp(item['create_time']).strftime('%Y%m%d %H:%M:%S')
        print(f"{pre}[{item['author__nickname']}]-{item['desc_']}-{item['statistics__digg_count']}-{create_time}\n"
              f"{item['share_url']}")


class testDouyinManager(unittest.TestCase):
    def test_list_items_by_digg_count(self):
        DouyinManager().list_items_by_digg_count()

    def test_print_item(self):
        item = DouyinItem()
        item['create_time'] = 1525576962
        DouyinManager().print_item(item)
