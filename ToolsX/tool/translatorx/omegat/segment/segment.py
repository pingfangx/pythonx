import re
from typing import List


def break_translation(translation: dict) -> dict:
    """分割翻译"""
    result = {}
    for k, v in translation.items():
        result.update(break_paragraph(k, v))
    return result


def break_paragraph(en: str, cn: str) -> dict:
    """
    分割片断
    org.omegat.core.segmentation.Segmenter#breakParagraph
    在 OmegaT 中有复杂的分割规则，这里简单分割一下
    """
    # 要保留符号，所以使用了捕获组
    # 结果不分割，所以加上了 (?=.)
    en_splits = _split(r'([.?!]+)(?=.)', en)
    cn_splits = _split(r'([。？！]+)(?=.)', cn)
    result = {}
    if len(en_splits) == len(cn_splits):
        for i in range(len(en_splits)):
            result[en_splits[i]] = cn_splits[i]
    else:
        result[en] = cn
    return result


def _split(pattern: str, sentence: str) -> List[str]:
    """分割，分割后还要保留符号
    参考 https://blog.csdn.net/pippo_liang/article/details/60955874
    """
    splits = re.split(pattern, sentence)
    n = len(splits)
    if n & 1 == 1:
        n += 1
        splits.append('')
    splits = [splits[i] + splits[i + 1] for i in range(0, n - 1, 2)]
    return splits
