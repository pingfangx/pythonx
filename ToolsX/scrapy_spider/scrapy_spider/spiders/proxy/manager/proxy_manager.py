import asyncio
import queue
import time
from unittest import TestCase

from scrapy_spider.common.pipeline.postgresql_manager import PostgreSQLManager
from scrapy_spider.spiders.proxy.items import ProxyItem


class ProxyManager:

    def __init__(self):
        item = ProxyItem()
        self.table_name = item.get_table_name()
        self.manager = PostgreSQLManager(item)
        self._proxy_queue = queue.Queue()

        # 一些 sql
        # 按使用次数排序，保存都能用到
        # TODO 修改
        self._sql_fetch_available = item.generate_get_sql() + """
        WHERE available=1
        OR (available=2 AND EXTRACT(EPOCH from NOW()- INTERVAL'1 HOUR') > banned_time)
        ORDER BY used_times LIMIT 10
        """

        """获取可用的"""

        primary_key = item.get_primary_key()
        self._sql_update = f"""
        UPDATE {item.get_table_name()}
        %s
        WHERE {primary_key} = {{{primary_key}}}
        """
        """后面的 3 个 {} 先求中间值，外面 2 个{{}}表示 1 个{} 用于格式化"""

        self._sql_update_used_times = self._sql_update % 'SET used_times=used_times+1 ,update_time={now}'
        """更新使用次数"""

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
            for record in record_list:
                item = ProxyItem(**record)
                self._proxy_queue.put(item)

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
        self._execute(self._sql_update_used_times, proxy)
        return proxy

    def success(self, proxy):
        """成功时调用"""
        self._execute(self._sql_update_success, proxy)

    def banned(self, proxy):
        """被禁时调用"""
        self._execute(self._sql_update_banned, proxy)

    def fail(self, proxy):
        """失败时调用"""
        self._execute(self._sql_update_fail, proxy)

    def remove(self, proxy: ProxyItem):
        """删除"""
        self._execute(proxy.generate_delete_sql())

    # 以下为私有方法
    def _execute(self, sql, proxy=None):
        """执行"""
        if proxy:
            sql = sql.format(now=int(time.time()), **proxy)
        print(f'执行 {sql}')
        asyncio.get_event_loop().run_until_complete(self.manager.execute(sql))


# 唯一实例
proxy_manager = ProxyManager()


class TestProxyManager(TestCase):
    item = ProxyItem(id='2')

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
        print(ProxyManager()._sql_fetch_available)
        print(ProxyManager()._sql_update)
        print(ProxyManager()._sql_update_used_times)
        print(ProxyManager()._sql_update_success)
        print(ProxyManager()._sql_update_fail)
        print(ProxyManager()._sql_update_banned)
