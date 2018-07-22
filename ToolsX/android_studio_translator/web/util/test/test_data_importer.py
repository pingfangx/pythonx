from unittest import TestCase

from android_studio_translator.web.model.translator.segment import Segment
from android_studio_translator.web.util.data_importer import DataImporter
from android_studio_translator.web.util.time_logger import TimeLogger


class TestDataImporter(TestCase):
    segment_list_file = 'segment_list.json'

    def test_parse_tmx_time(self):
        result = DataImporter().parse_tmx_time('20180721T120019Z')
        print(result)

    # 弃用

    def test_save_segment_list_to_json_file(self):
        segment_list = []
        for i in range(10):
            s = Segment()
            s.source = f's{i}'
            segment_list.append(s.__dict__)
        DataImporter.save_segment_list_to_json_file(segment_list, self.segment_list_file)

    def test_load_segment_list_from_json_file(self):
        time_logger = TimeLogger('从 json 读取')
        segment_list = DataImporter().load_segment_list_from_json_file(self.segment_list_file)
        print(f'共 {len(segment_list)} 条')
        time_logger.stop()
