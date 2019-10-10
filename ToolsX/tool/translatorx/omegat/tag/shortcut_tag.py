import re

from twisted.trial import unittest


def shortcut_tag_of_file(file, output):
    """处理文件"""
    import translatorx_utils
    translation = translatorx_utils.get_translation_dict_from_omegat_file(file)
    translation = shortcut_tag_of_translation(translation)
    translatorx_utils.save_translation_dict_to_omegat_file(translation, output)


def shortcut_tag_of_translation(translation: dict) -> dict:
    """按 OmegaT 的规则缩短标签

    简单处理，不考虑嵌套的情况
    """
    result = {}
    for k, v in translation.items():
        result[shortcut_tag(k)] = shortcut_tag(v)
    return result


def shortcut_tag(sentence: str) -> str:
    if not sentence:
        return sentence
    n = 0

    def replace(match):
        nonlocal n
        tag = match.group(1)  # type:str
        tag = tag[0].lower() + str(n)
        n += 1
        return f'<{tag}>{match.group(2)}</{tag}>'

    pattern = r'<([a-zA-Z]+)>(.+?)</\1>'  # 因为会被替换为数字，所以不能使用 \w
    while re.search(pattern, sentence):  # 因为可能嵌套，所以不能直接 sub，要用 while
        sentence = re.sub(pattern, replace, sentence)
    return sentence


class _Test(unittest.TestCase):
    def test_shortcut_tag_of_file(self):
        shortcut_tag_of_file(
            file=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update.tmx',
            output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update-shortcut-tag.tmx',
        )
