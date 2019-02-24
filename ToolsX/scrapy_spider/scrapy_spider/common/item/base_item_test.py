from twisted.trial import unittest


class BaseItemTest(unittest.TestCase):
    item = None
    """用于测试的 item"""

    def test_generate_create_table_sql(self):
        print(self.item.generate_create_table_sql())

    def test_generate_insert_formatter_sql(self):
        print(self.item.generate_insert_formatter_sql())
