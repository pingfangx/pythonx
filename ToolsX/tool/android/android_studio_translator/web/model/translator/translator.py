from tool.android.android_studio_translator import BaseTranslatorModel


class Translator(BaseTranslatorModel):
    """翻译者
    用来记录译者参与的项目，以及项目参与的译者"""
    user = ''
    """译者"""
    user_id = 0
    """译者id"""
    project_id = 0
    """参与项目id"""
    translate_count = 0
    """
    参与该项目翻译数
    表示参照机器翻译进行人工翻译"""
    review_count = 0
    """参与该项目审核数"""
    advice_count = 0
    """
    参与该项目建议数
    表示对现有翻译提出修改建议"""
