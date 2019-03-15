import datetime
import time
import unittest
import webbrowser

from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLHelper
from scrapy_spider.spiders.douyin.items import DouyinItem


class DouyinManager:
    """数据管理"""

    def __init__(self):
        item = DouyinItem()
        self.table_name = item.get_table_name()
        self.helper = PostgreSQLHelper(item)

    @staticmethod
    def get_last_watch_days_before_today():
        """上一次看的天数"""
        try:
            with open('../log/log.txt', 'r') as f:
                last_line = f.readlines()[-1]
                last_day = last_line.split('-')[1]
                now = datetime.datetime.today()
                today_zero = datetime.datetime(now.year, now.month, now.day)
                last_day_zero = datetime.datetime(int(last_day[0:4]), int(last_day[4:6]), int(last_day[6:8]))
                return (today_zero - last_day_zero).days
        except IOError:
            pass
        return 1

    def list_items_by_digg_count(self, start_days_before_today=1, end_days_before_today=0, limit=10, offset=0):
        """按点赞次数
        :param start_days_before_today: 开始时间，多少天
        :param end_days_before_today: 结束时间，多少天
        :param limit: 限制
        :param offset: 偏移
        """

        # 计算时间
        now = datetime.datetime.today()
        if start_days_before_today == 0:
            # 未指定开始时间，获取所有
            start_time = 0
            end_time = now.timestamp()
        else:
            # 当天 0 时
            today_zero = datetime.datetime(now.year, now.month, now.day)
            start_day = today_zero - datetime.timedelta(days=start_days_before_today)
            start_time = start_day.timestamp()
            end_day = today_zero - datetime.timedelta(days=end_days_before_today)
            end_time = end_day.timestamp()
        with open('../log/log.txt', 'a') as f:
            f.writelines('\n%s-%s' % (datetime.datetime.fromtimestamp(start_time).strftime('%Y%m%d'),
                                      datetime.datetime.fromtimestamp(end_time).strftime('%Y%m%d')))
        sql = f"""
        SELECT id,author__nickname,desc_,statistics__digg_count,share_url,create_time FROM {self.table_name}
        WHERE create_time >= {start_time} AND create_time < {end_time}
        ORDER BY statistics__digg_count DESC
        LIMIT {limit} OFFSET {offset}
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
                self.print_item(item, f'{i + 1}/{length} ')

    def print_item(self, item: DouyinItem, pre=''):
        create_time = datetime.datetime.fromtimestamp(item['create_time']).strftime('%Y%m%d %H:%M:%S')
        url = item['share_url']
        url = url.replace('.iesdouyin.', '.amemv.')
        print(f"[{create_time}] {pre}[{item['id']}] [{item['author__nickname']}]-"
              f"{item['desc_']}-[{item['statistics__digg_count']}]\n"
              f"{url}")
        self.open_in_browser(url)

    def open_in_browser(self, url):
        webbrowser.open_new_tab(url)
        time.sleep(0.5)


class TestDouyinManager(unittest.TestCase):

    def test_list_items_by_digg_count_auto(self):
        days = DouyinManager.get_last_watch_days_before_today()
        if days == 0:
            print('已看到当天')
            return
        DouyinManager().list_items_by_digg_count(start_days_before_today=days, end_days_before_today=days - 1,
                                                 limit=10, offset=0)

    def test_list_items_by_digg_count(self):
        DouyinManager().list_items_by_digg_count(start_days_before_today=7, end_days_before_today=6, limit=20, offset=0)

    def test_print_item(self):
        print()
        item = DouyinItem()
        item['create_time'] = 1525576962
        DouyinManager().print_item(item)
