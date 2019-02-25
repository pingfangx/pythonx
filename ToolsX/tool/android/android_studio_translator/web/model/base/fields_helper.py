import inspect
import re
from typing import Dict


class Field:
    """字段"""

    def __init__(self, name: str, type: str, extra: str, comment: str, default_value=None):
        """

        :param name:字段名
        :param type:类型
        :param extra:额外设置
        :param comment:注释
        :param default_value:默认值
        """
        self.name = name
        self.type = type
        self.extra = extra
        self.comment = comment
        self.default_value = default_value
        if self.default_value is None:
            if 'INT' in self.type.upper():
                self.default_value = 0
            else:
                self.default_value = ''

    def __str__(self):
        return '{' + ','.join([f'{k}={v}' for k, v in self.__dict__.items()]) + '}'

    def __repr__(self):
        return self.__str__()


class FieldsHelper:
    """用来解析字段的描述"""

    def __init__(self, cls=None):
        self.fields_dict: Dict[str, Field] = {}
        self.cls = cls
        if cls:
            self.parse_class(cls)

    def parse_class(self, cls):
        """解析后才能调用其他方法"""
        if not inspect.isclass(cls):
            cls = cls.__class__
            self.cls = cls

        # 判断是否有缓存
        if cls in cached_fields_dict.keys():
            # 已经有解析结果了
            self.fields_dict = cached_fields_dict[cls]
            return
        # 没有缓存，进行解析
        # 解析所有父类
        for c in inspect.getmro(cls):
            # 不处理 object
            if c != object:
                self.parse_text(inspect.getsource(c))

        # 如果超限，随机删除一个
        if len(cached_fields_dict) >= 100:
            cached_fields_dict.popitem()
        # 保存解析结果
        cached_fields_dict[cls] = self.fields_dict

    def parse_text(self, text: str):
        """"解析源码"""
        # 将后面的方法过滤
        text = text[:text.find('def ')]
        # 空格 字母 空格 = 内容 3个" 内容 3个"
        pattern = re.compile(r'\s{4}(\w+)\s*=(.*?)"{3}(.+?)"{3}', re.S)
        all_match = re.findall(pattern, text)
        if not all_match:
            return
        for name, value, comment in all_match:
            if name not in self.fields_dict.keys():
                type = None
                if name == 'create_time':
                    type = 'TIMESTAMP'
                    extra = 'NOT NULL DEFAULT CURRENT_TIMESTAMP'
                elif name == 'update_time':
                    type = 'TIMESTAMP'
                    extra = 'NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
                else:
                    comment_list = comment.split('\n')
                    comment_length = len(comment_list)
                    if comment_length == 1:
                        # 只有一行，视为注释
                        extra = 'NOT NULL'
                        comment = comment_list[0]
                    else:
                        # 多于一行，取前 2 行作为类型，注释
                        type, comment = comment_list[0:2]
                        if ',' in type:
                            # 如果包括逗号，分为类型与额外的
                            type, extra = type.split(',')[0:2]
                        else:
                            if 'NOT NULL' in type:
                                extra = ''
                            else:
                                extra = 'NOT NULL'
                # 去除空格
                comment = comment.strip()
                # 去除空格与换行
                value = value.strip(' \n')
                if '\'' in value:
                    # 字符串
                    value = value.strip('\'')
                else:
                    # 不包启单引号
                    value = int(value)
                # 不管单行、多行，对类型进行默认处理
                if not type:
                    if name.endswith('_id') or name.endswith('_ip') or name.endswith('_count') \
                            or name.startswith('segments_'):
                        # id,ip,count 都保存为 int
                        type = 'INT UNSIGNED'
                    elif name.endswith('user'):
                        type = 'VARCHAR(15)'
                    else:
                        type = 'TEXT'
                self.fields_dict[name] = Field(name, type, extra, comment, value)

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

    def __str__(self):
        return f'fields helper of {self.cls.__name__}'


cached_fields_dict = {}
"""缓存解析结果
解析是耗时操作（读取文件），所以根据类名进行缓存"""
