import datetime
import json
from xml.etree import ElementTree

from tool.android.android_studio_translator import Segment
from xx.database.mysql_model_helper import MySqlModelHelper


class SegmentUtil:
    """导入数据"""

    @staticmethod
    def save_segments(segment_list):
        """保存"""
        model_helper = MySqlModelHelper(Segment())
        model_helper.insert_item_list(segment_list)

    def load_segments_from_tmx_file(self, file_path):
        """从 tmx 文件读取"""

        tree = ElementTree.parse(file_path)
        tmx = tree.getroot()
        body = tmx.find('body')
        result = []
        for tu in body.iter('tu'):
            segment = Segment()
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'EN-US':
                    # 取英文
                    segment.source = tuv.find('seg').text
                elif tuv.attrib['lang'] == 'ZH-CN':
                    # 取中文
                    segment.target = tuv.find('seg').text
                    segment.create_user = tuv.attrib['creationid']
                    segment.create_time = self.parse_tmx_time(tuv.attrib['creationdate'])
                    segment.update_user = tuv.attrib['changeid']
                    segment.update_time = self.parse_tmx_time(tuv.attrib['changedate'])
            result.append(segment)
        return result

    @staticmethod
    def parse_tmx_time(tmx_date) -> str:
        """用于将 tmx 中记录的 GMT 时间转为 UTC 时间
        :return str，因为最终数据库类型为 TIMESTAMP，所以直接格式化为字符串"""
        time = datetime.datetime.strptime(tmx_date, '%Y%m%dT%H%M%SZ')
        # 加 8 小时
        time = time + datetime.timedelta(hours=8)
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def save_segment_list_to_json_file(segment_list, json_file):
        """保存进 json 文件，一开始是因为从 tmx 解析太慢了
        后来发现是因为初始化的原因，修改后不再需要保存进 json"""
        with open(json_file, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(segment_list, default=lambda x: x.__dict__))

    @staticmethod
    def dict_to_segment(data):
        segment = Segment()
        segment.__dict__ = data
        return segment

    def load_segment_list_from_json_file(self, json_file):
        """从 json 文件读取"""
        with open(json_file, encoding='utf-8') as f:
            return json.loads(f.read(), object_hook=self.dict_to_segment)
