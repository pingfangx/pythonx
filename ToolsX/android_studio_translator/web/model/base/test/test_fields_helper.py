from unittest import TestCase

from android_studio_translator.web.model.base.base_model import BaseModel
from android_studio_translator.web.model.base.fields_helper import FieldsHelper
from android_studio_translator.web.model.translator.project import Project


class TestFieldsHelper(TestCase):
    def test_parse_base_model(self):
        print(FieldsHelper(BaseModel).fields_dict.items())

    def test_parse_project(self):
        print(FieldsHelper(Project).fields_dict.items())
