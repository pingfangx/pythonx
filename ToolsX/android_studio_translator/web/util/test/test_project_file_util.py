import re
from unittest import TestCase

from android_studio_translator.web.model.translator.project_file import ProjectFile
from android_studio_translator.web.util.project_file_util import ProjectFileUtil
from android_studio_translator.web.util.time_logger import TimeLogger
from xx.database.mysql_model_helper import MySqlModelHelper


class TestProjectFileUtil(TestCase):
    source_dir = r'D:\workspace\TranslatorX\JetBrains\source'
    ignore_pattern_list = [
        re.compile('\.gitkeep'),
        re.compile('\.(?!properties)')
    ]
    test_object = ProjectFileUtil(source_dir, 1, ignore_pattern_list)

    def test_list_project_file(self):
        file_list = self.test_object.list_project_file()
        print(f'共 {len(file_list)} 个文件')
        for file in file_list:
            print(file.name)

    def test_save_file_list(self):
        file_list = self.test_object.list_project_file()
        print(f'共 {len(file_list)} 个文件')
        model_helper = MySqlModelHelper(ProjectFile())
        model_helper.create_table()
        time_logger = TimeLogger('写入数据库')
        model_helper.insert_item_list(file_list)
        time_logger.stop()

    def test_get_project_file_list(self):
        print(self.test_object.get_project_file_list())

    def test_prepare_file_segment_dict(self):
        self.test_object.prepare_file_segment_dict()
        print(self.test_object.prepare_file_segment_dict())
