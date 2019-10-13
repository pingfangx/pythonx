from bs4 import BeautifulSoup

from omegat.align.html_parser.html_parser import AlignHtmlParser


class Bs4Parser(AlignHtmlParser):
    """继承父类

    主要问题是如何收集 tag
    使用迭代，依次累加 tag
    """

    def __init__(self, parser='html.parser', debug=False):
        super().__init__(debug)
        self.parser = parser

    def feed(self, data):
        soup = BeautifulSoup(data, self.parser)
        self.iter_tag(soup.find('html'), [])

    def iter_tag(self, root, tags):
        if isinstance(root, str):
            self.process_tag(tags, root)
            return
        children = list(root.children)
        if len(children) == 0:
            self.process_tag(tags, root.text)
        else:
            for i, child in enumerate(children):
                self.iter_tag(child, tags + [root.name])

    def process_tag(self, pre_tags, text):
        self._tag_stack = pre_tags  # 赋值给父类
        tag = pre_tags[-1]  # 最后一个即是当前标签
        if text.strip():
            self.print(f'添加临时内容【{text}】')
            self.tmp_data.append(text)
        self.check_and_process_tag(tag)
