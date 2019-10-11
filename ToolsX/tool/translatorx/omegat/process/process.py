import re

from twisted.trial import unittest


def replace_space(sentence: str) -> str:
    """替换空格"""
    return sentence.replace('\xa0', ' ')


def shortcut_tag(sentence: str) -> str:
    """缩短标签"""
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
        sentence = re.sub(pattern, replace, sentence, count=1)  # 指定 count 1 按顺序替换，否则可能交错
    return sentence


def process_of_file(file, output, process):
    """处理文件"""
    import translatorx_utils
    translation = translatorx_utils.get_translation_dict_from_omegat_file(file)
    translation = process_of_translation(translation, process)
    if output:
        translatorx_utils.save_translation_dict_to_omegat_file(translation, output)


def process_of_translation(translation: dict, process) -> dict:
    result = {}
    for k, v in translation.items():
        result[process(k)] = process(v)
    return result


class _Test(unittest.TestCase):
    def test_shortcut_tag(self):
        print(shortcut_tag(''))

    def test_shortcut_tag_of_file(self):
        process_of_file(
            file=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update.tmx',
            output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update-shortcut-tag.tmx',
            process=shortcut_tag
        )

    def test_process_space_of_file(self):
        process_of_file(
            file=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Deprecated.tmx',
            output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Deprecated-remove_space.tmx',
            process=replace_space
        )
