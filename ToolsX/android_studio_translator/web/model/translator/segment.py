from android_studio_translator.web.model.translator.base_translator_model import BaseTranslatorModel


class Segment(BaseTranslatorModel):
    """翻译片段
    翻译的基本单位，不与项目关联，应该独立，然后可以供多个项目使用"""
    source = ''
    """原语言内容"""
    target = ''
    """翻译结果"""
    status = 0
    """TINYINT
    翻译状态"""
    create_user = ''
    """创建者"""
    create_user_id = 0
    """创建者id"""
    update_user = ''
    """更新者"""
    update_user_id = 0
    """更新者id"""
    review_user = ''
    """审核者"""
    review_user_id = 0
    """审核者id"""
