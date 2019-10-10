import re

from twisted.trial import unittest


def update_from_level2(file, output):
    with open(file, encoding='utf-8') as f:
        text = f.read()
        text = text.replace('xml:lang', 'lang')  # 替换语言标签
        text = re.sub(r'<[be]pt.*?/>', '', text)  # 替换 bpt 和 ept
        with open(output, 'w', encoding='utf-8') as of:
            of.write(text)
            print(f'写入 {output}')


class _Test(unittest.TestCase):
    def test_update_from_level2(self):
        update_from_level2(
            file=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6.tmx',
            output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\Java-api-1.6-update.tmx',
        )
