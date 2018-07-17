from unittest import TestCase

from android_studio_translator.web.model.base.base_model import BaseModel
from android_studio_translator.web.model.base.fields_helper import fields_helper
from android_studio_translator.web.model.translator.project import Project


class TestFieldsHelper(TestCase):
    def test_parse(self):
        fields_helper.parse(Project)
        print(fields_helper.fields_dict)
        print(fields_helper.get_desc('name'))

    def test_parse_super(self):
        fields_helper.parse(BaseModel)
        print(fields_helper.get_desc('id'))
