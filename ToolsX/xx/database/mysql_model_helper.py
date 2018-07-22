from typing import List

from android_studio_translator.web.model.base.base_model import BaseModel
from xx.database.mysql_helper import MySqlHelper


class MySqlModelHelper(MySqlHelper):
    def __init__(self, model):
        super().__init__()
        self.model: BaseModel = model

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
