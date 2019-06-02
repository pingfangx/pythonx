import asyncio
import queue

import asyncpg
from asyncpg import Connection

from scrapy_spider.common.config import postgre_configs
from scrapy_spider.common.item.base_item import BaseItem


class PostgreSQLManager:
    """
    PostgreSQL 管理连接、插入等
    插入是否可以优化为保存一定量，再批量插入
    """
    conn: Connection
    """连接"""

    create_table_sql: str = ''
    """建表 sql"""

    cached_commands = []
    cached_commands_limit = 10
    cached_commands_q = queue.Queue()

    def __init__(self, item=None, configs=None, transaction=False):
        self.configs = configs
        if self.configs is None:
            self.configs = postgre_configs
        self.transaction = transaction
        if item is not None:
            self.create_table_sql = item.generate_create_table_sql()

    async def prepare(self):
        """准备"""
        await self.connect_database()
        await self.create_table()

    async def connect_database(self):
        """连接"""
        self.conn = await asyncpg.connect(**self.configs)

    async def close_connect(self):
        """关闭"""
        if self.transaction:
            await self.execute_transaction()
        if self.conn is not None:
            await self.conn.close()

    async def create_table(self):
        """建表"""
        await self.execute(self.create_table_sql)

    async def insert_item(self, item: BaseItem):
        await self.execute(item.generate_insert_sql())

    async def update_item(self, item: BaseItem):
        await self.execute(item.generate_update_sql())

    async def fetch(self, sql):
        """获取"""
        return await self.conn.fetch(sql)

    async def execute(self, sql):
        """执行 sql """
        if not sql:
            return
        if self.transaction:
            self.cached_commands.append(sql)
            if len(self.cached_commands) >= self.cached_commands_limit and self.cached_commands_q.empty():
                # 转移到队列，防止未执行完还没清空，又有新 sql
                print('执行事务')
                await self.execute_transaction()
        else:
            await self.conn.execute(sql)

    async def execute_transaction(self):
        for sql in self.cached_commands:
            self.cached_commands_q.put(sql)
        self.cached_commands.clear()
        tr = self.conn.transaction()
        await tr.start()
        try:
            while not self.cached_commands_q.empty():
                await self.conn.execute(self.cached_commands_q.get())
        except Exception:
            print('执行 sql 出错')
            await tr.rollback()
            raise
        finally:
            await tr.commit()


class PostgreSQLHelper(PostgreSQLManager):
    """助手类

    封装一层
    """

    def __init__(self, item=None):
        super().__init__(item)
        self.prepare()

    def prepare(self):
        return asyncio.get_event_loop().run_until_complete(super().prepare())

    def close_connect(self):
        return asyncio.get_event_loop().run_until_complete(super().close_connect())

    def fetch(self, sql):
        return asyncio.get_event_loop().run_until_complete(super().fetch(sql))

    def insert_item(self, item: BaseItem):
        return asyncio.get_event_loop().run_until_complete(super().insert_item(item))

    def update_item(self, item: BaseItem):
        return asyncio.get_event_loop().run_until_complete(super().update_item(item))
