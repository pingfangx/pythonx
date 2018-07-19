from android_studio_translator.web.model.translator.project import Project
from android_studio_translator.web.model.translator.tests.test_sql import TestSql


class TestProject(TestSql):
    def test_insert(self):
        project = Project()
        project.name = '一' * 20
        self.execute(project.generate_insert_formatter_sql().format(**project.__dict__))
