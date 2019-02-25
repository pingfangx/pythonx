from typing import List

from xx.database.mysql_helper import MySqlHelper
from .model.base_model import BaseModel


class MySqlModelHelper(MySqlHelper):
    def __init__(self, model):
        super().__init__()
        self.model: BaseModel = model
        self.table_name = self.model.get_table_name()

    def create_table(self):
        """建表"""
        self.execute(self.model.generate_create_table_sql())

    def insert_item(self, item: BaseModel):
        """插入数据"""
        self.execute(item.generate_insert_sql())

    def insert_item_list(self, item_list: List[BaseModel]):
        """批量插入数据"""
        with self.conn.cursor() as cursor:
            for item in item_list:
                cursor.execute(item.generate_insert_sql())
        self.conn.commit()

    def select_all(self, sql=None):
        """选择全部"""
        if sql is None:
            sql = self.model.generate_select_sql()
        return self.fetchall(sql, True)

    def select_one(self, sql=None, asc=True):
        """选择一条"""
        if sql is None:
            sql = self.model.generate_select_sql(asc=asc)
        return self.fetchone(sql, True)

    def select_first(self, sql=None):
        """选择第一条"""
        return self.select_one(sql, True)

    def select_last(self, sql=None):
        """选择最后一条"""
        return self.select_one(sql, False)
