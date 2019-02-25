import re

from tool.android.android_studio_translator import Segment
from tool.android.android_studio_translator import TestSql
from tool.android.android_studio_translator.web.util import SegmentUtil
from tool.android.android_studio_translator.web.util import TimeLogger
from xx.database.mysql_helper import MySqlHelper


class TestExecuteMany(TestSql):
    def test_execute_many(self):
        """批量插入性能测试
        [Python MySQLdb 循环插入execute与批量插入executemany性能分析](https://blog.csdn.net/colourless/article/details/41444069)
        实测两种方法差不多，另外还介绍了 load data infile 方法
        """
        tmx_file = r'D:\workspace\TranslatorX\JetBrains\omegat\project_save.tmx'
        time_logger = TimeLogger('解析 tmx ')
        segment_list = SegmentUtil().load_segments_from_tmx_file(tmx_file)
        time_logger.stop()
        print(f'共 {len(segment_list)} 条数据')
        self.test_insert_1(segment_list)
        self.test_insert_2(segment_list)

    def test_insert_1(self, segment_list):
        mysql_helper = MySqlHelper()

        time_logger = TimeLogger('循环插入')
        conn = mysql_helper.conn
        with conn.cursor() as cursor:
            length = len(segment_list)
            for i in range(length):
                if i % 1000 == 0:
                    print(f'execute {i+1}/{length}')
                segment = segment_list[i]
                try:
                    cursor.execute(segment.generate_insert_sql())
                except Exception as e:
                    print(e)
                    print(segment.generate_insert_sql())
        conn.commit()
        time_logger.stop()

    def test_insert_2(self, segment_list):
        segment = Segment()
        insert_sql = segment.generate_insert_formatter_sql()
        insert_sql = re.sub('\'?{.*?}\'?', '%s', insert_sql)
        print(insert_sql)
        mysql_helper = MySqlHelper()

        time_logger = TimeLogger('executemany')
        conn = mysql_helper.conn
        with conn.cursor() as cursor:
            length = len(segment_list)
            args = []
            for i in range(length):
                if i % 1000 == 0:
                    print(f'execute {i+1}/{length}')
                segment = segment_list[i]
                # 要注意顺序
                args.append([v for v in segment.generate_insert_formatter_dict().values()])
            try:
                cursor.executemany(insert_sql, args)
            except Exception as e:
                print(e)
        conn.commit()
        time_logger.stop()
