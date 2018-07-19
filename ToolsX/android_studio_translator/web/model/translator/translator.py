from android_studio_translator.web.model.translator.base_translator_model import BaseTranslatorModel


class Translator(BaseTranslatorModel):
    """翻译者
    用来记录译者参与的项目，以及项目参与的译者"""
    user = ''
    """译者"""
    user_id = 0
    """译者id"""
    project_id = 0
    """参与项目id"""
    manual_count = 0
    """参与该项目人工翻译数"""
    review_count = 0
    """参与该项目人工审核数"""
    advice_count = 0
    """参与该项目建议修改数"""
