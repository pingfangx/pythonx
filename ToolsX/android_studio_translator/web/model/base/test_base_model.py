from unittest import TestCase

from android_studio_translator.web.model.base.base_model import BaseModel
from xx.database.mysql_helper import MySqlHelper


class TestBaseModel(TestCase):
    test_obj = BaseModel()

    def test_generate_create_table_sql(self):
        print(self.test_obj.generate_create_table_sql())

    def test_create_table(self):
        sql = self.test_obj.generate_create_table_sql()
        helper = MySqlHelper()
        helper.execute(sql)

    def test_generate_insert_formatter_sql(self):
        print(self.test_obj.generate_insert_formatter_sql())

    def test_generate_delete_sql(self):
        self.test_obj.id = 22
        print(self.test_obj.generate_delete_sql())
