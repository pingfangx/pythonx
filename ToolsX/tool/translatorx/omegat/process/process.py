import re

from twisted.trial import unittest


def replace_space(sentence: str) -> str:
    """替换空格"""
    return sentence.replace('\xa0', ' ')


def shortcut_tag_of_translation(translation: dict) -> dict:
    result = {}
    for k, v in translation.items():
        tags = {}
        k = shortcut_tag(k, tags)  # 需要先算 k 收集 tags
        v = shortcut_tag(v, tags)
        result[k] = v
    return result


def shortcut_tag(sentence: str, tags: dict) -> str:
    """
    缩短标签
    :param tags: 顺序可能不一致，所以中文应该参照英文的顺序
    为空时缩短的同时收集标签
    """
    if not sentence:
        return sentence
    n = 0

    collect_tags = {}
    duplicate = False

    def replace(match):
        nonlocal n, duplicate
        tag = match.group(1)  # type:str
        if tags:  # 直接比较
            if tag in tags:
                tag = tags[tag]
            else:
                tag = tag[0].lower() + str(n)
        else:  # 收集标签
            if tag in collect_tags:
                duplicate = True
            collect_tags[tag] = tag[0].lower() + str(n)
            tag = collect_tags[tag]
        n += 1
        return f'<{tag}>{match.group(2)}</{tag}>'

    # 这里贪婪和懒惰都不能实现，如 <code><code>test</code></code> 和 <code>test</code><code>test2</code>
    # 只能用栈吧
    # 弄巧成拙的是，由于中英文都生成的不对，由于插入模糊匹配时会尝试替换标签，所以又正确替换了
    pattern = r'<([a-zA-Z]+)>(.+?)</\1>'  # 因为会被替换为数字，所以不能使用 \w
    while re.search(pattern, sentence):  # 因为可能嵌套，所以不能直接 sub，要用 while
        sentence = re.sub(pattern, replace, sentence, count=1)  # 指定 count 1 按顺序替换，否则可能交错
    if not tags and not duplicate:  # 不重复可以更新
        tags.update(collect_tags)
    return sentence


def filter_incorrect_translation(translation: dict) -> dict:
    """过滤不正确的翻译

    一个英文翻译成了另一个英文
    """
    result = {}
    chinese_pattern = re.compile(u'([\u4e00-\u9fa5])')
    for k, v in translation.items():
        if k != v:
            if not re.search(chinese_pattern, k) and not re.search(chinese_pattern, v):
                # 没有中文，却不相等，认为翻译不正确
                # print(f'认为译文不正确【{k}】->【{v}】')
                continue
        if '\x02' in v:  # 特殊字符 OmageT 无法处理，特殊情况替换
            v = v.replace("'\x02apos;", "'\\u002E'")
        result[k] = v
    return result


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
        tags = {}
        print(shortcut_tag(r'', tags))
        print(shortcut_tag(r'', tags))

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
