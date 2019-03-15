import asyncio
import queue
import time
from unittest import TestCase

from scrapy_spider.common.log import log
from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLManager
from scrapy_spider.spiders.douyin import douyin_spider
from scrapy_spider.spiders.proxy.items import ProxyItem


class ProxyManager:

    def __init__(self):
        item = ProxyItem()
        self.manager = PostgreSQLManager(item)
        self.max_fail_time = 5
        self._proxy_queue = queue.Queue()

        # 一些 sql
        table_name = item.get_table_name()
        available_condition = """
        WHERE available=1
        OR (available=2 AND EXTRACT(EPOCH from NOW()- INTERVAL'1 HOUR') > banned_time)
        """
        # 按使用次数排序，保存都能用到

        # 要让并发每次都能取到，如果每次请求 1s，则每隔 1s 就可能重复取到 ip
        # 乘以 10，可以让 10 轮请求后，才会重复
        limit = douyin_spider.CONCURRENT_REQUESTS * 10
        if limit > 200:
            limit = 200
        self._sql_fetch_available = item.generate_get_sql() + available_condition + f"""
        ORDER BY used_times LIMIT {limit}
        """
        """获取可用的"""

        self._sql_count = f"""
        SELECT COUNT(*) FROM {table_name}
        """
        """统计数量"""

        self._sql_available_count = f"""
        SELECT COUNT(*) FROM {table_name}
        {available_condition}
        """
        """统计有效数量"""

        primary_key = 'ip'
        self._sql_update = f"""
        UPDATE {table_name}
        %s
        WHERE {primary_key} = '{{{primary_key}}}'
        """
        """后面的 3 个 {} 先求中间值，外面 2 个{{}}表示 1 个{} 用于格式化"""

        self._sql_get_fail_times_by_ip = f"""
        SELECT fail_times FROM {table_name}
        WHERE {primary_key} = '{{{primary_key}}}'
        """
        """获取失败次数"""

        self._sql_add_times = self._sql_update % 'SET {key}={key}+1 ,update_time={now}'
        """添加次数"""

        self._sql_update_success = self._sql_update % 'SET success_times=success_times+1 ,' \
                                                      ' update_time={now} , available=1'
        """更新为成功"""

        self._sql_update_fail = self._sql_update % 'SET update_time={now} , available=0'
        """更新为失败"""

        self._sql_update_banned = self._sql_update % 'SET fail_times=fail_times+1 ,' \
                                                     ' banned_time={now} , update_time={now} , available=2'
        """更新为被禁"""

        # 初始化
        asyncio.get_event_loop().run_until_complete(self.manager.connect_database())
        asyncio.get_event_loop().run_until_complete(self.manager.create_table())

    async def fetch(self, sql):
        record_list = await self.manager.fetch(sql)
        if record_list:
            print(f'读取到 ip {len(record_list)} 个')
            for record in record_list:
                item = ProxyItem(**record)
                self._proxy_queue.put(item)

    def count(self):
        """计算数量"""
        return asyncio.get_event_loop().run_until_complete(self.manager.conn.fetchval(self._sql_count))

    def available_count(self):
        """计算可用数量"""
        return asyncio.get_event_loop().run_until_complete(self.manager.conn.fetchval(self._sql_available_count))

    def get(self):
        """获取代理"""
        while self._proxy_queue.empty():
            # 执行获取
            asyncio.get_event_loop().run_until_complete(self.fetch(self._sql_fetch_available))
            if self._proxy_queue.empty():
                # 如果还为空，等待获取
                sleep_time = 60
                print(f'当前代理为空，sleep {sleep_time}')
                time.sleep(sleep_time)
        # 循环结束，肯定不为空
        proxy = self._proxy_queue.get()
        # 更新使用次数
        self._execute(self._sql_add_times, proxy, key='used_times')
        print(f'当前 ip {self.available_count()}/{self.count()}')
        return proxy

    def success(self, proxy: ProxyItem):
        """成功时调用"""
        log.info(f'{proxy} success')
        self._execute(self._sql_update_success, proxy)

    def banned(self, proxy: ProxyItem):
        """被禁时调用"""
        log.info(f'{proxy} banned')
        self._execute(self._sql_update_banned, proxy)

    def fail(self, proxy: ProxyItem):
        """失败时调用"""
        # 添加失败次数
        self._execute(self._sql_add_times, proxy, key='fail_times')
        # 获取失败次数
        sql = self._sql_get_fail_times_by_ip.format(**proxy)
        record = asyncio.get_event_loop().run_until_complete(self.manager.conn.fetchrow(sql))
        if record:
            fail_times = record['fail_times']
            if fail_times and fail_times >= self.max_fail_time:
                # 大于指定次数，置为不可用
                log.info(f'{proxy} fail {fail_times} times set available=0')
                self._execute(self._sql_update_fail, proxy)
            else:
                log.info(f'{proxy} fail set fail_times={fail_times}')

    def remove(self, proxy: ProxyItem):
        """删除"""
        self._execute(proxy.generate_delete_sql())

    # 以下为私有方法
    def _execute(self, sql, proxy=None, key=None):
        """执行"""
        if proxy:
            if isinstance(proxy, str):
                sql = sql.format(now=int(time.time()), key=key, **ProxyItem.parse(proxy))
            elif isinstance(proxy, ProxyItem):
                sql = sql.format(now=int(time.time()), key=key, **proxy)
        # print(f'执行 {sql}')
        asyncio.get_event_loop().run_until_complete(self.manager.execute(sql))


# 唯一实例
proxy_manager = ProxyManager()


class TestProxyManager(TestCase):
    item = ProxyItem(ip='123')

    def test_count(self):
        print(ProxyManager().count())

    def test_available_count(self):
        print(ProxyManager().available_count())

    def test_get(self):
        proxy = ProxyManager().get()
        print(proxy)

    def test_remove(self):
        ProxyManager().remove(self.item)

    def test_success(self):
        ProxyManager().success(ProxyItem(self.item))

    def test_fail(self):
        ProxyManager().fail(ProxyItem(self.item))

    def test_banned(self):
        ProxyManager().banned(ProxyItem(self.item))

    def test_sql(self):
        pm = proxy_manager
        for k, v in pm.__dict__.items():
            if k.startswith('_sql'):
                print(f'{k} = {v}')
