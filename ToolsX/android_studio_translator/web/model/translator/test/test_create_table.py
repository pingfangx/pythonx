from android_studio_translator.web.model.translator.project import Project
from android_studio_translator.web.model.translator.project_file import ProjectFile
from android_studio_translator.web.model.translator.project_file_segment import ProjectFileSegment
from android_studio_translator.web.model.translator.project_file_statistics import ProjectFileStatistics
from android_studio_translator.web.model.translator.project_statistics import ProjectStatistics
from android_studio_translator.web.model.translator.segment import Segment
from android_studio_translator.web.model.translator.segment_log import SegmentLog
from android_studio_translator.web.model.translator.test.test_sql import TestSql
from android_studio_translator.web.model.translator.translator import Translator


class TestCreateTable(TestSql):
    """测试建表"""

    def test_create_table_project(self):
        self.execute(Project().generate_create_table_sql())

    def test_create_table_project_statistics(self):
        self.execute(ProjectStatistics().generate_create_table_sql())

    def test_create_table_project_file(self):
        self.execute(ProjectFile().generate_create_table_sql())

    def test_create_table_project_file_statistics(self):
        self.execute(ProjectFileStatistics().generate_create_table_sql())

    def test_create_table_project_file_segment(self):
        self.execute(ProjectFileSegment().generate_create_table_sql())

    def test_create_table_segment(self):
        self.execute(Segment().generate_create_table_sql())

    def test_create_table_segment_log(self):
        self.execute(SegmentLog().generate_create_table_sql())

    def test_create_table_translator(self):
        self.execute(Translator().generate_create_table_sql())
