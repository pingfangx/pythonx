from tool.android.android_studio_translator import BaseTranslatorModel


class ProjectFile(BaseTranslatorModel):
    """项目文件"""
    project_id = 0
    """对应项目id"""
    name = ''
    """文件名"""
    path = ''
    """
    文件目录
    虽然唯一，但不适合作 key"""
