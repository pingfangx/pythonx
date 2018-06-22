from xx import iox
from xx import systemx


class Field:
    """字段"""

    def __init__(self, name, _type, comment):
        """
        :param name: 名字
        :param _type: 类型
        :param comment: 注释
        """
        self.name = name.strip()
        self._type = _type.strip()
        self.comment = comment.strip()

    def get_name_str(self):
        """名字"""
        return self.name

    def get_method_name_str(self):
        """获取方法名，将首字母大写"""
        return self.name[:1].upper() + self.name[1:]

    def get_type_str(self):
        """类型，可能会进行替换"""
        result = self._type
        # 日期保存为 Long
        result = result.replace('Date', 'Long')
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
    /**
     * {comment}
     */
    private {type} {name};
        """.format(**self.get_format_dict())

    def get_get_method_str(self) -> str:
        """get 方法"""
        return """ 
    /**
     * @return {comment}
     */       
    public {type} get{method}() {{
        return {name};
    }}
        """.format(**self.get_format_dict())

    def get_set_method_str(self):
        """set 方法"""
        return """ 
    /**
     * 
     * @param {name} {comment}
     */
    public void set{method}({type} {name}) {{
        this.{name} = {name};
    }}
        """.format(**self.get_format_dict())


class ParseWikiToBean:
    """解析 wiki 为 bean"""

    def __init__(self, text, line_separator='\n', separator='\t', include_field=True, include_get=True,
                 include_set=False):
        """
        :param text:文本，以指定分符分隔，默认为 \t
        名字\t类型\t描述
        :param line_separator: 行分隔符
        :param separator: 各属性分隔符
        :param include_field: 是否包生成字段
        :param include_get: 是否包生成 get 方法
        :param include_set: 是否包生成 set 方法
        """
        self.text = text
        self.line_separator = line_separator
        self.separator = separator
        self.include_field = include_field
        self.include_get = include_get
        self.include_set = include_set

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
                    field_list.append(Field(name, _type, comment))
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


if __name__ == '__main__':
    wiki_text = """
labelId	Long	标签ID	 
labelName	String	标签名	 
    """
    ParseWikiToBean(wiki_text).main()
