from tool.android.android_studio_translator import BaseTranslatorModel


class ProjectFileSegment(BaseTranslatorModel):
    """项目文件中的片段"""
    project_id = 0
    """项目id"""
    file_id = 0
    """
    文件id
    文件 id 可能为0，只指定项目id
    只有项目id时，片断应该不重复，同名的片段只能有一个翻译
    拥有文件id时，同名的片段可以在不同文件中有不同的翻译"""
    segment_id = 0
    """片段id"""
