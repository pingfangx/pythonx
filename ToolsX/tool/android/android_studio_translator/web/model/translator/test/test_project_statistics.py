from unittest import TestCase

from tool.android.android_studio_translator import ProjectStatistics
from tool.android.android_studio_translator import Segment, SegmentStatusEnum
from xx.database.mysql_model_helper import MySqlModelHelper


class TestProjectStatistics(TestCase):
    def test_project_statistics(self):
        """项目统计，正式时应该由操作更新，导入时读取数据库更新"""
        segment_model_helper = MySqlModelHelper(Segment())
        table_name = segment_model_helper.table_name

        project_statistics = ProjectStatistics()

        # 目标 id
        project_statistics.target_id = 1

        id_range = (0, 999999)
        """插入数据的范围 (start,end]"""
        id_range_condition = f'id>{id_range[0]} AND id<={id_range[1]}'

        # 片段数
        result = segment_model_helper.fetchone(
            f"SELECT COUNT(*) FROM {table_name} WHERE {id_range_condition}")
        print(f'count={result[0]}')
        project_statistics.segments_all = result[0]

        # 译者数
        result = segment_model_helper.fetchall(
            f'SELECT update_user,update_user_id,COUNT(1) FROM {table_name}'
            f' WHERE {id_range_condition} GROUP BY update_user,update_user_id')
        for user, user_id, count in result:
            # 每一个作者，需要插入作者表
            print(user, user_id, count)
        project_statistics.translator_count = len(result)

        # 状态
        result = segment_model_helper.fetchall(
            f'SELECT `status`,COUNT(1) FROM {table_name} WHERE {id_range_condition} GROUP BY `status`')
        for status, count in result:
            print(status, count)
            # 第一种状态
            if status == SegmentStatusEnum.MACHINE_TRANSLATED_2.value:
                project_statistics.segments_machine = count
            elif status == SegmentStatusEnum.MANUAL_TRANSLATED_3.value:
                project_statistics.segments_manual = count
            elif status == SegmentStatusEnum.ADVICE_4.value:
                project_statistics.segments_advice = count
        print(project_statistics)
