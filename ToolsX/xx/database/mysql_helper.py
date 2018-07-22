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

    def fetchone(self, sql, as_dict=False):
        """
        获取
        :param sql:
        :param as_dict: 是否处理为字典
        是否返回字典，否则返回元组
        :return:
        """
        print(f'执行 {sql}')
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            item = cursor.fetchone()
            if not as_dict:
                return item
            else:
                return self.tuple_item_to_dict(item, cursor)

    def fetchall(self, sql, as_dict):
        """
        获取全部
        :param sql:
        :param as_dict: 是否处理为字典
        是否返回字典列表，否则返回元组列表
        :return:
        """
        print(f'执行 {sql}')
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            item_list = cursor.fetchall()
            if not as_dict:
                return item_list
            else:
                return [self.tuple_item_to_dict(item, cursor) for item in item_list]

    @staticmethod
    def tuple_item_to_dict(item, cursor):
        """sql 返回的 元组根据 cursor 转为字典"""
        result = {}
        for i in range(len(item)):
            result[cursor.description[i][0]] = item[i]
        return result

    def close(self):
        """关闭"""
        self.conn.close()
