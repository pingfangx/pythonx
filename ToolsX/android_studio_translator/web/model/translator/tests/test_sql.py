import unittest

from xx.database.mysql_helper import MySqlHelper


class TestSql(unittest.TestCase):
    """测试 sql"""

    execute_sql = True
    """是否执行 sql，如果为 False ，则只输出"""

    def execute(self, sql, execute=True):
        """
        :param sql:
        :param execute: 用于单个方法可以先传 False 控制
        :return:
        """
        if execute and self.execute_sql:
            # 执行
            MySqlHelper().execute(sql)
        else:
            print(sql)
