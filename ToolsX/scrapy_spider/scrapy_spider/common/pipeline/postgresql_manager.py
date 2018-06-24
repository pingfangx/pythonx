import asyncpg
from scrapy_spider.common.ignore.postgre_config import postgre_configs
from scrapy_spider.common.item.base_item import BaseItem


class PostgreSQLManager:
    """
    PostgreSQL 管理连接、插入等
    插入是否可以优化为保存一定量，再批量插入
    """

    def __init__(self, item=None, create_table_sql=None, insert_formatter_sql=None, configs=None):
        if configs is None:
            configs = postgre_configs
        self.configs = configs
        if item is not None:
            self.create_table_sql = item.generate_create_table_sql()
            self.insert_formatter_sql = item.generate_insert_formatter_sql()
        # 不为 none 以指定的的为准，可能传了 item 但有一个需要修改
        if create_table_sql is not None:
            self.create_table_sql = create_table_sql
        if insert_formatter_sql is not None:
            self.insert_formatter_sql = insert_formatter_sql

        self.conn = None

    async def insert_item(self, item):
        for k in item.fields.keys():
            value = item[k]
            if isinstance(value, str):
                if "'" in value:
                    # 转义 '
                    value = value.replace("'", "''")
                    item[k] = value
        sql = self.insert_formatter_sql.format(**item)
        await self.execute(sql)

    async def execute(self, sql):
        """执行 sql
        TODO 是否需要事务？如何优化
        """
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.execute(sql)
        except Exception:
            print('执行 sql 出错')
            print(sql)
            await tr.rollback()
            raise
        finally:
            await tr.commit()

    async def connect_database(self):
        """
        连接
        """
        self.conn = await asyncpg.connect(**self.configs)

    async def close_connect(self):
        if self.conn is not None:
            await self.conn.close()

    async def create_table(self):
        """
        创建表
        """
        await self.execute(self.create_table_sql)

    @staticmethod
    def parse_name_type(name):
        return BaseItem.parse_name_type(name)
