from unittest import TestCase

from android_studio_translator.web.model.translator.segment import Segment


class TestBaseTranslatorModel(TestCase):
    def test_generate_insert_formatter_dict(self):
        model = Segment()
        model.create_user = model.update_user = model.review_user = 'pingfangx'
        print(model.generate_insert_sql())
