import re

from twisted.trial import unittest


def replace_special_word(file, output):
    edit_file(file, output, lambda x: x.replace("'\x02apos;", "'\\u002E'"))


def update_from_level2(file, output):
    def m(text: str) -> str:
        text = text.replace('xml:lang', 'lang')  # 替换语言标签
        text = re.sub(r'<[be]pt.*?/>', '', text)  # 替换 bpt 和 ept
        return text

    edit_file(file, output, m)


def edit_file(file, output, callback):
    with open(file, encoding='utf-8') as f:
        text = f.read()
        text = callback(text)
        with open(output, 'w', encoding='utf-8') as of:
            of.write(text)
            print(f'写入 {output}')


def replace_shortcut_tag(actual, en, cn):
    """替换缩短的标签"""
    p = re.compile(r'((<\w\d+>)+)(.+?)((</\w\d+>)+)')
    first, mid, last = 0, 2, 3
    actual_match_list = list(reversed(re.findall(p, actual)))  # 为了防止相同标签重复，倒序，从大到小替换
    en_match_list = list(reversed(re.findall(p, en)))
    if actual_match_list and en_match_list:
        if len(actual_match_list) == len(en_match_list):
            for i, actual_match in enumerate(actual_match_list):
                en_match = en_match_list[i]
                actual_word = actual_match[mid]
                en_word = en_match[mid]
                if actual_word == en_word:
                    print(f'文字相同 {en_word}')
                    find = en_match[first]
                    replace = actual_match[first]
                    print(f'尝试将 {find} 替换为 {replace}')
                    cn = cn.replace(find, replace)
                    find = en_match[last]
                    replace = actual_match[last]
                    print(f'尝试将 {find} 替换为 {replace}')
                    cn = cn.replace(find, replace)
    return cn


class _Test(unittest.TestCase):
    def test_replace_special_word(self):
        replace_special_word(
            r'',
            r'',
        )

    def test_update_from_level2(self):
        update_from_level2(
            file=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6.tmx',
            output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update.tmx',
        )

    def test_replace_shortcut_tag(self):
        print(replace_shortcut_tag(
            r'',
            r'',
            r'',
        ))
