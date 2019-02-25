from tool.android.android_studio_translator import Project
from tool.android.android_studio_translator import TestSql


class TestProject(TestSql):
    test_object = Project()

    def test_insert(self, execute=True):
        project = Project()
        project.thread_id = 2421
        project.name = 'JetBrains 系列软件汉化包'
        project.description = project.name
        project.project_url = 'https://github.com/pingfangx/TranslatorX'
        project.original_url = 'https://www.jetbrains.com/products.html'
        project.create_user = '平方X'
        project.create_user_id = 10001
        project.version = 'v2018.2'
        project.icon = ''
        self.execute(project.generate_insert_sql())
