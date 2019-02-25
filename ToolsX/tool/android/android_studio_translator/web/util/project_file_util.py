import os
import re
from typing import List, Dict

from tool.android.android_studio_translator import ProjectFile
from tool.android.android_studio_translator import ProjectFileSegment
from tool.android.android_studio_translator import Segment
from xx.database.mysql_model_helper import MySqlModelHelper


class ProjectFileUtil:

    def __init__(self, source_dir: str, project_id: int, ignore_pattern=None):
        """

        :param source_dir:源文件目录
        :param project_id:项目 id
        :param ignore_pattern:忽略正则或正则列表
        """
        self.source_dir = source_dir
        if not self.source_dir.endswith('\\'):
            # 拼接末尾的斜杠，保存时少一个字符
            self.source_dir += '\\'
        self.project_id = project_id
        self.ignore_pattern = ignore_pattern

        self.file_segment_dict: Dict[int, List[Segment]] = {}

    def list_project_file(self) -> List[ProjectFile]:
        """
        列出项目中的文件
        :return: List[ProjectFile]
        """
        result = []
        for parent, dir_names, file_names in os.walk(self.source_dir):
            for file in file_names:
                if self.ignore_file(file, self.ignore_pattern):
                    continue
                file_path = os.path.join(parent, file).replace(self.source_dir, '')
                project_file = ProjectFile()
                project_file.project_id = self.project_id
                project_file.name = file
                project_file.path = file_path
                result.append(project_file)
        return result

    @staticmethod
    def ignore_file(file_name, ignore_pattern):
        """
        是否忽略文件
        :param file_name: 文件名
        :param ignore_pattern: 忽略正则或正则列表
        :return:
        """
        if not ignore_pattern:
            return False
        if isinstance(ignore_pattern, list):
            for pattern in ignore_pattern:
                if re.search(pattern, file_name):
                    return True
        else:
            if re.search(ignore_pattern, file_name):
                return True
        return False

    def parse_segment_list(self, segment_list: List[Segment]):
        """解析片段列表"""
        self.prepare_file_segment_dict()
        project_file_segment_list = []
        for segment in segment_list:
            source = segment.source
            for file_id, file_segment_list in self.file_segment_dict.values():
                if source in file_segment_list:
                    project_file_segment = ProjectFileSegment()
                    project_file_segment.project_id = self.project_id
                    project_file_segment.file_id = file_id
                    project_file_segment.segment_id = segment.id
                    project_file_segment_list.append(project_file_segment)
            # 存在

    def prepare_file_segment_dict(self):
        """准备片段字典"""
        if not self.file_segment_dict:
            project_file_list = self.get_project_file_list()
            self.file_segment_dict = self.get_file_segment_dict(project_file_list)

    @staticmethod
    def get_project_file_list() -> List[ProjectFile]:
        """获取数据库中的文件列表"""
        model_helper = MySqlModelHelper(ProjectFile())
        sql = f'SELECT id,project_id,`name`,path FROM {model_helper.table_name} ORDER BY id ASC'
        return model_helper.select_all(sql)

    def get_file_segment_dict(self, file_list: List[ProjectFile]) -> Dict[int, List[Segment]]:
        """列出以 file 为 key 的片段字典"""
        segment_dict = {}
        length = len(file_list)
        for i in range(length):
            print(f'读取文件 {i+1}/{length}')
            project_file = file_list[i]
            file_path = os.path.join(self.source_dir, project_file.path)
            segment_dict[project_file.id] = ProjectFileUtil.get_segment_list_from_file(file_path)
        return segment_dict

    @staticmethod
    def get_segment_list_from_file(file_path) -> List[Segment]:
        """列出所有要翻译的源片段
        此处只针对 properties 中的格式"""
        result = []
        with open(file_path) as f:
            for line in f.readlines():
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                split_result = line.split('=')
                if len(split_result) == 2:
                    _, v = line.split('=')
                    result.append(v)
                else:
                    print(line)
                    exit()
        return result
