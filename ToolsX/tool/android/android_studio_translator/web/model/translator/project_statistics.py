from tool.android.android_studio_translator import BaseTranslatorModel


class ProjectStatistics(BaseTranslatorModel):
    """翻译项目统计
    与项目表分开，我也不知道为什么，只是觉得这个表会经常操作"""
    target_id = 0
    """对应的目标id"""
    translator_count = 0
    """译者数"""
    star_count = 0
    """点赞数"""
    file_count = 0
    """项目文件数"""
    segments_all = 0
    """片段总数"""
    segments_machine = 0
    """机器翻译数"""
    segments_manual = 0
    """人工翻译数"""
    segments_review = 0
    """人工审核数"""
    segments_advice = 0
    """建议修改数"""
