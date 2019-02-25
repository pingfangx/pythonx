from tool.android.android_studio_translator import BaseTranslatorModel


class Project(BaseTranslatorModel):
    """翻译项目"""
    thread_id = 0
    """对应帖子id"""
    name = ''
    """ VARCHAR(20)
    名字"""
    description = ''
    """VARCHAR(200)
    描述"""
    project_url = ''
    """VARCHAR(100)
    翻译项目地址
    指汉化结果的发布地址"""
    original_url = ''
    """VARCHAR(100)
    原始项目地址
    指汉化源的地址"""
    create_user = ''
    """创建者"""
    create_user_id = 0
    """创建者id"""
    version = ''
    """VARCHAR(10)
    版本"""
    icon = ''
    """VARCHAR(100)
    图标"""
