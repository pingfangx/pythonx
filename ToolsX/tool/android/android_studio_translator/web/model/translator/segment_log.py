from tool.android.android_studio_translator import BaseTranslatorModel


class SegmentLog(BaseTranslatorModel):
    """翻译片段操作日志"""
    segment_id = 0
    """片断id"""
    target_id = 0
    """
    操作对象id
    可以用来记录审核了哪一条提交"""
    action_type = 0
    """TINYINT
    操作类型"""
    action_content = ''
    """操作内容"""
    action_comment = ''
    """VARCHAR(20)
    操作备注"""
    action_user = ''
    """操作者"""
    action_user_id = 0
    """操作者id"""
    action_user_ip = 0
    """
    操作者ip
    类型为 int，注意转换，可用于限制操作"""
    action_result = 0
    """TINYINT
    操作结果
    用来记录审核通过或拒绝
    """
