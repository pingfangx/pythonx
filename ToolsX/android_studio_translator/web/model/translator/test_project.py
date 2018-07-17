from unittest import TestCase

from android_studio_translator.web.model.translator.project import Project
from android_studio_translator.web.model.translator.project_statistics import ProjectStatistics
from android_studio_translator.web.model.translator.segment import Segment
from android_studio_translator.web.model.translator.segment_log import SegmentLog
from android_studio_translator.web.model.translator.translator import Translator
from xx.database.mysql_helper import MySqlHelper


class TestTranslatorProject(TestCase):
    test_object = Project()
    execute = False

    def test_create_table_project(self):
        self.print_sql(Project().generate_create_table_sql())

    def test_create_table_project_statistics(self):
        self.print_sql(ProjectStatistics().generate_create_table_sql())

    def test_create_table_segment(self):
        self.print_sql(Segment().generate_create_table_sql())

    def test_create_table_segment_log(self):
        self.print_sql(SegmentLog().generate_create_table_sql())

    def test_create_table_translator(self):
        self.print_sql(Translator().generate_create_table_sql())

    def print_sql(self, sql):
        print(sql)
        if self.execute:
            # 执行
            MySqlHelper().execute(sql)
