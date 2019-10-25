from twisted.trial import unittest

from omegat.align import BaseAlign
from omegat.align.html_parser.html_parser import AlignHtmlParser


class HtmlAlign(BaseAlign):
    """ Html 文件
    总有部分标签不执行 handle_endtag，造成不对应
    """
    name = 'html'
    print_info = True

    def __init__(self, debug=False):
        self.debug = debug

    def create_parser(self, file):
        parser = AlignHtmlParser(debug=self.debug)
        with open(file) as f:
            parser.feed(f.read())
        return parser

    def align_inner(self, source, target) -> dict:
        source_parser = self.create_parser(source)
        target_parser = self.create_parser(target)
        source_data = source_parser.get_data()
        target_data = target_parser.get_data()
        self.print(f'源文件共有 {len(source_data)} 条内容')
        self.print(f'结果文件共有 {len(target_data)} 条内容')
        target_unique = dict(filter(lambda x: x[0] not in source_data.keys(), target_data.items()))
        source_data = dict(filter(lambda x: x[0] in target_data.keys(), source_data.items()))
        target_data = dict(filter(lambda x: x[0] in source_data.keys(), target_data.items()))
        if self.debug:
            self.print(f'过滤后')
            self.print(f'源文件共有 {len(source_data)} 条内容')
            self.print(f'结果文件共有 {len(target_data)} 条内容')
            self.print('=' * 30 + '以下是键值对比' + '=' * 30)
            self.print_dif(source_parser.get_data(), target_parser.get_data())

            self.print(f'结果文件独有的内空 {len(target_unique)} 条内容')
            self.print('=' * 30 + '以下是独有内容' + '=' * 30)
            for k, v in target_unique.items():
                self.print(k)
                self.print(v)

        result = {}
        for k, v in source_data.items():
            en = v
            cn = target_data[k]
            result[en] = cn
        return result

    def print(self, msg):
        if self.debug:
            print(msg)

    def print_dif(self, source: dict, target: dict):
        for i, (k, v) in enumerate(zip(source.items(), target.items())):
            print(i)
            print('\n'.join(k))
            print('\n'.join(v))


class _Test(unittest.TestCase):
    def test(self):
        translation = HtmlAlign(debug=True).align(
            source=r'D:\software\program\java\jdk1.6.0_45\en改\docs\api\java\util\concurrent\atomic\package-summary.html',
            target=r'D:\software\program\java\jdk1.6.0_45\cn\docs\api\java\util\concurrent\atomic\package-summary.html'
        )
        print(f'结果为')
        for i, (k, v) in enumerate(translation.items()):
            print(i)
            print(k)
            print(v)
