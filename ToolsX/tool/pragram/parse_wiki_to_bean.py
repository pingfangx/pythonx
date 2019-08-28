from xx import iox
from xx import systemx


class Field:
    """字段"""

    def __init__(self, name, _type: str, comment, convert_zero=False):
        """
        :param name: 名字
        :param _type: 类型
        :param comment: 注释
        :param convert_zero: 是否将 Long 或 Integer 的 get 方法返回 0
        """
        self.name = name.strip()
        self._type = _type.strip()
        # 日期保存为 Long
        self._type = self._type.replace('Date', 'Long')
        self._type = self._type.capitalize().replace('number', 'Integer')
        self.comment = comment.strip()
        self.convert_zero = convert_zero

    def get_name_str(self):
        """名字"""
        return self.name

    def get_method_name_str(self):
        """获取方法名，将首字母大写"""
        return self.name[:1].upper() + self.name[1:]

    def get_type_str(self):
        """类型，可能会进行替换"""
        result = self._type
        return result

    def get_comment_str(self):
        """注释"""
        return self.comment

    def get_format_dict(self):
        """用于格式化"""
        return {
            'name': self.get_name_str(),
            'type': self.get_type_str(),
            'comment': self.get_comment_str(),
            'method': self.get_method_name_str()
        }

    def get_field_str(self) -> str:
        """字段声明"""
        return """
    /** {comment} */
    private {type} {name};""".format(**self.get_format_dict())

    def get_get_method_str(self) -> str:
        """get 方法"""
        if self.convert_zero:
            if self._type == 'Long' or self._type == 'Integer':
                format_dict = self.get_format_dict()
                format_dict['type'] = format_dict['type'].replace('Long', 'long').replace('Integer', 'int')
                return """
    public {type} get{method}OrZero() {{
        return {name} == null ? 0 : {name};
    }}
                """.format(**format_dict)
        return """
    public {type} get{method}() {{
        return {name};
    }}
        """.format(**self.get_format_dict())

    def get_set_method_str(self):
        """set 方法"""
        return """
    public void set{method}({type} {name}) {{
        this.{name} = {name};
    }}
        """.format(**self.get_format_dict())


class ParseWikiToBean:
    """解析 wiki 为 bean"""

    def __init__(self, text, line_separator='\n', separator='\t', include_field=True, include_get=True,
                 include_set=False, convert_zero=False):
        """
        :param text:文本，以指定分符分隔，默认为 \t
        名字\t类型\t描述
        :param line_separator: 行分隔符
        :param separator: 各属性分隔符
        :param include_field: 是否包生成字段
        :param include_get: 是否包生成 get 方法
        :param include_set: 是否包生成 set 方法
        :param convert_zero: 是否将 Long 或 Integer 的 get 方法返回 0
        """
        self.text = text
        self.line_separator = line_separator
        self.separator = separator
        self.include_field = include_field
        self.include_get = include_get
        self.include_set = include_set
        self.convert_zero = convert_zero

    def main(self):
        action_list = [
            ['退出', exit],
            ['解析', self.parse, self.text],
        ]
        iox.choose_action(action_list)

    def parse(self, text):
        """解析"""
        field_list = []
        lines = text.split(self.line_separator)
        for line in lines:
            if line:
                split_result = line.split(self.separator)
                if len(split_result) >= 3:
                    name, _type, comment = split_result[:3]
                    field_list.append(Field(name, _type, comment, self.convert_zero))
        result = ''
        if self.include_field:
            for field in field_list:
                result += field.get_field_str()
        if self.include_get:
            for field in field_list:
                result += field.get_get_method_str()
        if self.include_set:
            for field in field_list:
                result += field.get_set_method_str()
        systemx.copy(result)


def parse_yapi_data(text):
    """yapi 格式的转换"""
    text = text.replace('\n非必须\n', '')
    text = text.replace('\n必须\n', '')
    return text


if __name__ == '__main__':
    wiki_text = """
labelCode	string	
必须
标签编码（operation：运营;sgmw:sgmw官方;juncar:骏认证用户,advisor:顾问;live:播主）	
labelName	string	
必须
标签名称	
labelValue	integer	
必须
标签的值 0：否 1：是	
labelBelong	string	
必须
标签所属ID	
labelBelongName	string	
必须
标签所属名称	
    """
    wiki_text = parse_yapi_data(wiki_text)
    ParseWikiToBean(wiki_text, include_set=False, convert_zero=True).main()
