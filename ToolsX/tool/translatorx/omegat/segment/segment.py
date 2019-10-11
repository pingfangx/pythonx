import re
from typing import List

from twisted.trial import unittest


def process_of_file(file, output):
    """处理文件"""
    import translatorx_utils
    translation = translatorx_utils.get_translation_dict_from_omegat_file(file)
    print(f'分割前 {len(translation)} 项')
    translation = break_translation(translation)
    print(f'分割后 {len(translation)} 项')
    if output:
        translatorx_utils.save_translation_dict_to_omegat_file(translation, output)


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
    # 结尾不分割 (?=.)，1.1 样式的不分割 (?!\d)
    # 于是改为后面不是数字 (?=\D)
    # 英文后面需要空格
    en_splits = _split(r'([.?!]+)(?=\s)', en)
    cn_splits = _split(r'([。？！]+)(?=\D)', cn)
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


class _Test(unittest.TestCase):
    def test_process_of_file(self):
        process_of_file(
            r'',
            r'',
        )
