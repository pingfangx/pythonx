from android_studio_translator.web.model.translator.base_translator_model import BaseTranslatorModel


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
    original_url = ''
    """VARCHAR(100)
    原始项目地址"""
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
