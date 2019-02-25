from enum import Enum, unique

from tool.android.android_studio_translator import BaseTranslatorModel


@unique
class SegmentStatusEnum(Enum):
    """片断状态枚举"""
    DEFAULT_0 = 0
    """默认"""
    CREATED_1 = 1
    """新建"""
    MACHINE_TRANSLATED_2 = 2
    """机器翻译"""
    MANUAL_TRANSLATED_3 = 3
    """人工翻译"""
    ADVICE_4 = 4
    """建议"""
    REVIEW_ACCEPTED_5 = 5
    """审核通过"""
    REVIEW_REFUSED_6 = 6
    """审核拒绝"""


class Segment(BaseTranslatorModel):
    """翻译片段
    翻译的基本单位，不与项目关联，应该独立，然后可以供多个项目使用
    对于多语言的片段翻译，由于没有用到，暂时不作处理，
    如果以后要添加，可以添加翻译类型字段，同时建立翻译类型表即可，比如前 2 位表示源语言，后 2 位表示目标语言"""
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

    def get_insert_ignore_keys(self):
        """创建时间可更新时间，可以插入"""
        return [
            self.get_primary_key(),
            'field_helper',
        ]

    def generate_insert_formatter_dict(self):
        """处理字典"""
        r = super().generate_insert_formatter_dict()
        if not r['review_user']:
            # review 为空
            r['review_user'] = r['update_user']
            r['review_user_id'] = r['update_user_id']
        if r['status'] == 0:
            # 没有状态
            r['status'] = SegmentStatusEnum.MANUAL_TRANSLATED_3.value
        return r
