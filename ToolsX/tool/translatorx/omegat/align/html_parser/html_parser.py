import re
from html.parser import HTMLParser


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

    def __init__(self, debug=False, ignore_p=False, ignore_b=False):
        super().__init__()
        self.debug = debug
        self.ignore_p = ignore_p
        self.ignore_b = ignore_b
        """是否忽加入 p 标签，有部分文件 p 没有结尾，多个 p 连在一起，需要忽略"""
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
        self.check_and_process_tag(tag)

    def check_process_p(self, tag: str) -> bool:
        """是否处理 p"""
        if self.ignore_p and tag.upper() == 'P':
            return False
        if self.ignore_b and tag.upper() == 'B':
            return False
        return True

    def check_and_process_tag(self, tag):
        if self.is_paragraph_tag(tag) and self.check_process_p(tag):
            data = self.contact_and_clear_tmp_data()
            if data:
                self.print(f'片段标签【{tag}】结束，添加内容【{data}】')
                self.add_data(data)
            self.tag_closed = True
        else:  # 非片段标签，记录
            if self.tmp_data:
                last = self.tmp_data[-1]
                # if len(tag) > 1:  # 过滤类似 b i
                if self.check_process_p(tag):
                    self.tmp_data[-1] = f'<{tag}>{last}</{tag}>'

    def handle_data(self, data: str):
        if data.strip():
            if self.tag_closed:
                self.print(f'当前开标签已关闭，直接添加内容【{data}】')
                self.add_data(data)
            else:
                # 2 个换行，因为在 add_data 中会进行分割
                if data.startswith(' - '):
                    data = '\n\n' + data[len(' - '):]
                if self.tmp_data:
                    last = re.sub(r'</?\w+>', '', self.tmp_data[-1])
                    if last in ['Returns:', '返回：', 'Throws:', '抛出：']:
                        self.tmp_data[-1] = '\n\n' + self.tmp_data[-1]  # 前面添加
                        data = '\n\n' + data  # 后面添加
                self.tmp_data.append(data)
                self.print(f'添加临时内容【{data}】')

    def contact_and_clear_tmp_data(self):
        """连接并清空临时数据"""
        s = ''.join(self.tmp_data)
        self.tmp_data.clear()
        return s

    def add_data(self, data):
        k = self.get_xpath_like_tag()
        # # 多个换行认为需要分割
        # 换行加多个空格也替换为换行，主要用于方法摘要中方法与说明
        # split_v = re.split(r'(\n{2,})|(\n(?=\s{10,}))', data)#可能中英文行数不一致
        split_v = re.split(r'(\n{2,})', data)
        content = []
        for i, v in enumerate(split_v):
            if not v or not v.strip():
                continue
            v = v.replace('\n', ' ')  # 这里替换换行与后面重新拼接换行不冲突
            v = re.sub(r'\s{2,}', ' ', v)  # 多个空格替换为单个
            v = v.strip()
            if v:
                content.append(v)
        v = '\n'.join(content)
        if v:
            self._data[k] = v  # 因为要使用相同的 tag 作为标记，所以划分好后，再用换行拼接，最后在由片段分割器分割
            self.print(f'添加内容【{v}】')
            if re.search(r'<tt>(.*?)</tt>', v):  # 在 api 1.6 中有部分 tt 标签被替换为 code 所以补充添加
                v = re.sub(r'<tt>(.*?)</tt>', r'<code>\1</code>', v)
                self._data[self.get_xpath_like_tag()] = v
                self.print(f'补充添加【{v}】')
            # 插入模糊匹配时会尝试自动替换，所以不再需要，只是影响 100% 的自动插入
            if re.search(r'<(a)><(code)>(.*?)</\2></\1>', v):  # api 1.6 与 Android api 中部分 a 和 code 相反
                v = re.sub(r'<(a)><(code)>(.*?)</\2></\1>', r'<\2><\1>\3</\1></\2>', v)
                self._data[self.get_xpath_like_tag()] = v
                self.print(f'补充添加 【{v}】')

    def get_xpath_like_tag(self) -> str:
        """只是用来标识，实际上不是 xpath 的格式"""
        xpath = '/'.join(self._tag_stack)
        xpath = xpath.replace('html/head/body/hr/table', 'html/head/body/table')  # StringBuilder cn改中缺少一个 hr
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
