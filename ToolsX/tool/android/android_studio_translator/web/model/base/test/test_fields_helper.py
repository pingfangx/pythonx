from unittest import TestCase

from tool.android.android_studio_translator import BaseModel
from tool.android.android_studio_translator import FieldsHelper
from tool.android.android_studio_translator import Project


class TestFieldsHelper(TestCase):
    def test_parse_base_model(self):
        print(FieldsHelper(BaseModel).fields_dict.items())

    def test_parse_project(self):
        print(FieldsHelper(Project).fields_dict.items())
