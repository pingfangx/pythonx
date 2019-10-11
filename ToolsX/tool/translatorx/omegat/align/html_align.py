import re
from html.parser import HTMLParser

from twisted.trial import unittest

from omegat.align import BaseAlign


class AlignHtmlParser(HTMLParser):
    """用于对齐的解析器

    为了判断是否是相同的内容，记录 tag 用于类似 xpath 的实现
    如果是相同的 xpath，也使用序号作为记录

    实现笔记
        在 handle_starttag 中标签入栈，在 handle_endtag 中出栈
        在 handle_data 中暂存数据（可能是段落的内部标签）
        出栈时，如果是段落标签，则添加暂存的数据
            添加时，用栈中的标签作为键，如果键相同，则认为中英文对齐
        如果不是段落标签，则将暂存数据的最后一个用标签包围
        后续再使用 segment 分割片段，使用 shortcut_tag 缩小标签
    """

    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        self._tag_stack = []
        self._xpath_dict = {}
        self._data = {}
        self.tmp_data = []
        self.tag_closed = False
        """标签关闭，在标签关闭、添加内容后置为 True
        在为 True 的时候，如果有内容，应该直接添加，不用暂存到 tmp_data
        """

    def ignore_tag(self, tag: str) -> bool:
        return tag.upper() in ['META']

    def handle_starttag(self, tag, attrs):
        if self.ignore_tag(tag):
            return
        self._tag_stack.append(tag)
        self.tag_closed = False

    def handle_endtag(self, tag):
        if self.ignore_tag(tag):
            return
        self._tag_stack.pop()
        if self.is_paragraph_tag(tag):
            data = self.contact_and_clear_tmp_data()
            self.print(f'片段标签结束，添加内容【{data}】')
            self.add_data(data)
            self.tag_closed = True
        else:  # 非片段标签，记录
            if self.tmp_data:
                last = self.tmp_data[-1]
                # if len(tag) > 1:  # 过滤类似 b i
                self.tmp_data[-1] = f'<{tag}>{last}</{tag}>'

    def handle_data(self, data: str):
        text = data.strip()
        if text:
            if self.tag_closed:
                self.print(f'当前开标签已关闭，直接添加内容【{data}】')
                self.add_data(data)
            else:
                self.tmp_data.append(text)
                self.print(f'添加临时内容【{text}】')

    def contact_and_clear_tmp_data(self):
        """连接并清空临时数据"""
        s = ''
        for i, data in enumerate(self.tmp_data):
            if i == 0:
                s += data
            else:
                ignore_space = False
                if len(data) == 1 and data in '.?!。？！':
                    # 如果加上单个符号，则不需要空格，所以不能用 join 来实现
                    ignore_space = True
                elif self.tmp_data[i - 1].endswith('>') and re.match('^[.?!,。？！，]', data):
                    # 以符号结尾，后面不需要添加标点符号
                    ignore_space = True
                if ignore_space:
                    s += data
                else:
                    s += ' ' + data
        self.tmp_data.clear()
        return s

    def add_data(self, data):
        k = self.get_xpath_like_tag()
        v = data
        v = v.replace('\n', ' ')
        v = re.sub(r'\s{2,}', ' ', v)  # 多个空格替换为单个
        if v:
            self._data[k] = v
            self.print(f'添加内容【{v}】')
            if re.search(r'<(a)><(code)>(.*?)</\2></\1>', v):
                v = re.sub(r'<(a)><(code)>(.*?)</\2></\1>', r'<\2><\1>\3</\1></\2>', v)
                self._data[self.get_xpath_like_tag()] = v
                self.print(f'补充添加 【{v}】')

    def get_xpath_like_tag(self) -> str:
        """只是用来标识，实际上不是 xpath 的格式"""
        xpath = '/'.join(self._tag_stack)
        if xpath in self._xpath_dict:
            self._xpath_dict[xpath] += 1
            return f'{xpath}/{self._xpath_dict[xpath]}'
        else:
            self._xpath_dict[xpath] = 0
            return xpath

    def get_data(self):
        """生成数据"""
        return self._data

    def is_paragraph_tag(self, tagname: str) -> bool:
        """org.omegat.filters2.html2.FilterVisitor#isParagraphTag"""
        tagname = tagname.upper()
        return tagname == "ADDRESS" or tagname == "BLOCKQUOTE" or tagname == "BODY" \
               or tagname == "CENTER" or tagname == "DIV" or tagname == "H1" \
               or tagname == "H2" or tagname == "H3" or tagname == "H4" \
               or tagname == "H5" or tagname == "H6" or tagname == "HTML" \
               or tagname == "HEAD" or tagname == "TITLE" or tagname == "TABLE" \
               or tagname == "TR" or tagname == "TD" or tagname == "TH" \
               or tagname == "P" or tagname == "PRE" or tagname == "OL" \
               or tagname == "UL" \
               or tagname == "LI" \
               or tagname == "DL" or tagname == "DT" \
               or tagname == "DD" \
               or tagname == "FORM" or tagname == "TEXTAREA" or tagname == "FIELDSET" \
               or tagname == "LEGEND" or tagname == "LABEL" or tagname == "SELECT" \
               or tagname == "OPTION" or tagname == "HR"

    def print(self, msg):
        if self.debug:
            print(msg)


class HtmlAlign(BaseAlign):
    """ Html 文件"""
    name = 'html'
    print_info = True

    def __init__(self, debug=False):
        self.debug = debug

    def align_inner(self, source, target) -> dict:
        source_parser = AlignHtmlParser(self.debug)
        target_parser = AlignHtmlParser(self.debug)
        with open(source) as f:
            source_parser.feed(f.read())
        with open(target) as f:
            target_parser.feed(f.read())
        source_data = source_parser.get_data()
        target_data = target_parser.get_data()
        self.print(f'源文件共有 {len(source_data)} 条内容')
        self.print(f'结果文件共有 {len(target_data)} 条内容')
        target_unique = dict(filter(lambda x: x[0] not in source_data.keys(), target_data.items()))
        source_data = dict(filter(lambda x: x[0] in target_data.keys(), source_data.items()))
        target_data = dict(filter(lambda x: x[0] in source_data.keys(), target_data.items()))
        self.print(f'过滤后')
        self.print(f'源文件共有 {len(source_data)} 条内容')
        self.print(f'结果文件共有 {len(target_data)} 条内容')
        self.print(f'结果文件独有的内空 {len(target_unique)} 条内容')
        if self.debug:
            self.print_dif(source_parser.get_data(), target_parser.get_data())
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
        for k, v in zip(source.items(), target.items()):
            print('\n'.join(k))
            print('\n'.join(v))


class _Test(unittest.TestCase):
    def test(self):
        translation = HtmlAlign(debug=True).align(
            source=r'D:\xx\software\program\java\jdk1.6\en\docs\api\java\nio\package-summary.html',
            target=r'D:\xx\software\program\java\jdk1.6\cn\docs\api\java\nio\package-summary.html'
        )
        print(f'结果为')
        print(translation)
