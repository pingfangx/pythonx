from android_studio_translator.web.model.translator.base_translator_model import BaseTranslatorModel


class SegmentLog(BaseTranslatorModel):
    """片断日志"""
    segment_id = 0
    """片断id"""
    action_id = 0
    """TINYINT
    操作id"""
    action_content = ''
    """操作内容"""
    action_user = ''
    """操作者"""
    action_user_id = 0
    """操作者id"""
    review_user = ''
    """审核者"""
    review_user_id = 0
    """审核者id"""
