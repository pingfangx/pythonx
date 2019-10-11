from omegat.align import BaseAlign
from omegat.align.item_align import ItemAlign


class IterAlign(BaseAlign):
    """检查是否是列表还是单个元素"""

    def align_inner(self, source, target) -> dict:
        translation = {}
        item_align = ItemAlign()
        # 要注意单个 str 也是可迭代的，所以不能用是否可迭代来判断
        if isinstance(source, list) and isinstance(target, list):
            for s, t in zip(source, target):
                translation.update(item_align.align(s, t))
        elif not isinstance(source, list) and not isinstance(target, list):
            translation = item_align.align(source, target)
        else:
            print('迭代类型不一致')
        return translation
