import inspect
import re
from typing import Dict


class Field:
    """字段"""

    def __init__(self, name, type, extra, comment):
        """

        :param name:字段名
        :param type:类型
        :param extra:额外设置
        :param comment:注释
        """
        self.name = name
        self.type = type
        self.extra = extra
        self.comment = comment


class FieldsHelper:
    """用来解析字段的描述"""

    def __init__(self, cls=None):
        self.fields_dict: Dict[str, Field] = {}
        if cls:
            self.parse_class(cls)

    def parse_class(self, cls):
        """解析后才能调用其他方法"""
        if not inspect.isclass(cls):
            cls = cls.__class__
        # 获取所有
        for cls in inspect.getmro(cls):
            # 不处理 object
            if cls != object:
                self.parse_text(inspect.getsource(cls))

    def parse_text(self, text: str):
        """"解析源码"""
        # 将后面的方法过滤
        text = text[:text.find('def ')]
        # 空格 字母 空格 = 内容 3个" 内容 3个"
        pattern = re.compile(r'\s{4}(\w+)\s*=.*?"{3}(.+?)"{3}', re.S)
        all_match = re.findall(pattern, text)
        if not all_match:
            return
        for name, comment in all_match:
            if name not in self.fields_dict.keys():
                if name == 'create_time':
                    type = 'timestamp'
                    extra = 'NOT NULL DEFAULT CURRENT_TIMESTAMP'
                elif name == 'update_time':
                    type = 'timestamp'
                    extra = 'NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
                else:
                    comment_list = comment.split('\n')
                    comment_length = len(comment_list)
                    if comment_length == 1:
                        # 只有一行
                        if name.endswith('_id') or name.endswith('_count') or name.startswith('segments_'):
                            type = 'INT UNSIGNED'
                        elif name.endswith('user'):
                            type = 'VARCHAR(15)'
                        else:
                            type = 'text'
                        extra = 'NOT NULL'
                        comment = comment_list[0]
                    else:
                        # 多于一行，只取前 2 行
                        type, comment = comment_list[0:2]
                        if 'NOT NULL' in type:
                            extra = ''
                        else:
                            extra = 'NOT NULL'
                comment = comment.strip()
                self.fields_dict[name] = Field(name, type, extra, comment)

    @staticmethod
    def camel_to_under_line(text):
        """驼峰转下划线"""
        result = ''
        for i in range(len(text)):
            c = text[i]
            if c.isupper():
                if i != 0:
                    result += '_'
                result += c.lower()
            else:
                result += c
        return result
