from html.parser import HTMLParser


class TradosHtmlParser(HTMLParser):
    """用于对齐的解析器

    为了判断是否是相同的内容，记录 tag 用于类似 xpath 的实现
    如果是相同的 xpath，也使用序号作为记录

    这个版本解析出来的结果很像 Trados 解析的结果，体现在
    A <tt>Closeable</tt> is a source or destination of data that can be closed.
    将变为 is a source or destination of data that can be closed.
    因为 A 与后面的属于同一层级，被覆盖
    <tt>Closeable</tt> 与后面在不同层级，被分开
    """

    def __init__(self):
        super().__init__()
        self._tag_stack = []
        self._xpath_dict = {}
        self._data = {}

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)

    def handle_endtag(self, tag):
        self._tag_stack.pop()

    def handle_data(self, data: str):
        text = data.strip()
        if text:  # 存入
            k = self.get_xpath_like_tag()
            self._data[k] = text

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
