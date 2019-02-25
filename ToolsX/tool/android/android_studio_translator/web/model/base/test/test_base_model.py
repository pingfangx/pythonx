from unittest import TestCase

from tool.android.android_studio_translator import BaseModel
from tool.android.android_studio_translator import Project
from tool.android.android_studio_translator import Segment
from xx.database.mysql_helper import MySqlHelper


class TestBaseModel(TestCase):
    test_obj = BaseModel()

    def test_default_values(self):
        print(self.test_obj.__dict__)

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

    def test_multi_object_field_helper(self):
        """测试多个对象的 field_helper 是否会影响"""
        print(BaseModel().generate_insert_sql())
        print(Project().generate_insert_sql())
        print(Segment().generate_insert_sql())
