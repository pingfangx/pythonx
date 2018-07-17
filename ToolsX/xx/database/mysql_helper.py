import pymysql

from xx.ignore.mysql_config import mysql_config


class MySqlHelper:
    """MySql 助手"""

    def __init__(self):
        self.conn = pymysql.connect(**mysql_config)

    def execute(self, sql):
        """执行"""
        print(f'执行 {sql}')
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        """关闭"""
        self.conn.close()
