import re
import time
import unittest

import scrapy


class BaseItem(scrapy.Item):
    """基类"""
    create_time_int4 = scrapy.Field()
    """创建时间"""

    update_time_int4 = scrapy.Field()
    """更新时间"""

    crawled_times_int4 = scrapy.Field()
    """爬取次数"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 需要更新
        self['create_time_int4'] = int(time.time())
        self['update_time_int4'] = int(time.time())
        # 不为空
        for k in self.fields.keys():
            if k not in self.keys() or self[k] is None:
                name, _type = self.parse_name_type(k)
                if _type == 'text':
                    self[k] = ""
                else:
                    self[k] = 0

    # get set 相关的方法
    def __setitem__(self, key, value):
        if key not in self.fields:
            key = self.check_key(key)
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if key not in self.fields:
            key = self.check_key(key)
        return super().__getitem__(key)

    def check_key(self, key):
        """
        尝试生成一个 key
        可能带类型
        """
        pattern = f'^{key}_int\d$'
        for k in self.fields.keys():
            if re.match(pattern, k):
                return k
        return key

    # 建表相关的方法
    def get_head_fields(self):
        """提前的字段，item 的字段将会按字母顺序排列，如果需要，则可以将其提前"""
        return None

    def get_tail_fields(self):
        """放在最后的字段"""
        return {
            'create_time_int4': '',
            'update_time_int4': '',
        }

    def get_on_conflict_suffix_sql(self):
        """获取冲突时添加在 insert 语句后的 sql"""
        sql = f"""
        ON CONFLICT(ip) DO UPDATE SET
        crawled_times={self.get_table_name()}.crawled_times+1,
        """
        sql += 'update_time={update_time_int4}'
        return sql

    def get_table_name(self):
        """获取表名"""
        return self.camel_to_under_line(self.__class__.__name__)

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

    @staticmethod
    def parse_name_type(name):
        """解析名字和类型"""
        match = re.match('^(.*)_(int\d)$', name)
        if match:
            return match.group(1), match.group(2)
        else:
            return name, 'text'

    def generate_create_table_sql(self):
        """
        生成建表的 SQL
        :return:
        """
        field_str = ''
        field_str += '"id" serial PRIMARY KEY NOT NULL,\n'

        head_fields = self.get_head_fields()
        # 填充头部字段
        if head_fields:
            for key in head_fields.keys():
                name, _type = self.parse_name_type(key)
                field_str += f'"{name}" {_type} {head_fields[key]} NOT NULL,\n'

        tail_fields = self.get_tail_fields()

        # 填充中间字段
        for key in self.fields.keys():
            if not head_fields or key not in head_fields.keys():
                if not tail_fields or key not in tail_fields.keys():
                    name, _type = self.parse_name_type(key)
                    field_str += f'"{name}" {_type} NOT NULL,\n'

        # 填充尾部字段
        if tail_fields:
            for key in tail_fields.keys():
                name, _type = self.parse_name_type(key)
                field_str += f'"{name}" {_type} {tail_fields[key]} NOT NULL,\n'

        # 去掉逗号
        field_str = field_str.rstrip(',\n')
        field_str += '\n'

        sql = f"CREATE TABLE IF NOT EXISTS {self.get_table_name()} (\n{field_str});"
        return sql

    def generate_insert_formatter_sql(self):
        """生成插入的 sql"""
        # 列出名字
        fields_list = []
        for k in self.fields.keys():
            name, _type = self.parse_name_type(k)
            fields_list.append(name)
        fields_list = ', '.join(fields_list)

        # 用 {} 包起来，后面用于格式化
        value_list = []
        for k in self.fields.keys():
            name, _type = self.parse_name_type(k)
            if _type == 'text':
                value_list.append("'{%s}'" % k)
            else:
                value_list.append("{%s}" % k)
        value_list = ', '.join(value_list)

        # 冲突处理
        on_conflict_extra_sql = self.get_on_conflict_suffix_sql()
        if on_conflict_extra_sql is None:
            on_conflict_extra_sql = ''

        sql = f'''
        INSERT INTO {self.get_table_name()} ({fields_list}) 
        VALUES ({value_list})
        {on_conflict_extra_sql};
        '''
        return sql


class BaseItemTest(unittest.TestCase):
    def test_get(self):
        item = BaseItem()
        item['create_time'] = 4
        self.assertEqual(item['create_time_int4'], 4)
        self.assertEqual(item['create_time'], 4)

    def test_default_value(self):
        print(BaseItem())

    def test_generate_create_table_sql(self):
        print(BaseItem().generate_create_table_sql())

    def test_generate_insert_formatter_sql(self):
        print(BaseItem().generate_insert_formatter_sql())
