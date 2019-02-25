from tool.android.android_studio_translator import Project
from tool.android.android_studio_translator import ProjectFile
from tool.android.android_studio_translator import ProjectFileSegment
from tool.android.android_studio_translator import ProjectFileStatistics
from tool.android.android_studio_translator import ProjectStatistics
from tool.android.android_studio_translator import Segment
from tool.android.android_studio_translator import SegmentLog
from tool.android.android_studio_translator import TestSql
from tool.android.android_studio_translator import Translator


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
