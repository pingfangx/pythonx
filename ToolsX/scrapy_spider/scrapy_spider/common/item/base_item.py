import re
import time
import unittest
from typing import Dict

import scrapy


class BaseItem(scrapy.Item):
    """基类"""
    id = scrapy.Field()
    """id，要注意创建表、插入语句要对其进行过滤"""

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

    # 工具方法
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

    def get_formatted_value(self, k):
        """获取格式化的值，用于 sql

        如果是 text 则拼上引号，并且转义 ' 为 ''
        """
        name, _type = self.parse_name_type(k)
        v = self[k]
        if _type == 'text':
            v = str(v).replace("'", "''")
            return f"'{v}'"
        else:
            return f'{v}'

    # 建表相关的方法
    def get_table_name(self):
        """获取表名"""
        return self.camel_to_under_line(self.__class__.__name__)

    def get_primary_key(self):
        """返回主键"""
        return 'id'

    def get_head_fields(self):
        """提前的字段，item 的字段将会按字母顺序排列，如果需要，则可以将其提前"""
        return None

    def get_tail_fields(self):
        """放在最后的字段"""
        return {
            'crawled_times_int4': '',
            'create_time_int4': '',
            'update_time_int4': '',
        }

    # 相关 sql

    def generate_create_table_sql(self):
        """
        生成建表的 SQL
        :return:
        """
        field_str = ''
        field_str += f'"{self.get_primary_key()}" serial PRIMARY KEY NOT NULL,\n'

        head_fields = self.get_head_fields()
        # 填充头部字段
        if head_fields:
            for key in head_fields.keys():
                name, _type = self.parse_name_type(key)
                field_str += f'"{name}" {_type} {head_fields[key]} NOT NULL,\n'

        tail_fields = self.get_tail_fields()

        # 填充中间字段
        for key in self.fields.keys():
            if key == self.get_primary_key():
                continue
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

    def generate_insert_sql(self):
        """生成插入的 sql"""
        # 列出名字
        fields_list = []
        for k in self.fields.keys():
            if k == self.get_primary_key():
                continue
            name, _type = self.parse_name_type(k)
            fields_list.append(name)
        fields_list = ', '.join(fields_list)

        # 列出值
        value_list = []
        for k in self.fields.keys():
            if k == self.get_primary_key():
                continue
            value_list.append(self.get_formatted_value(k))
        value_list = ', '.join(value_list)

        # 冲突处理
        on_conflict_extra_sql = self.get_on_conflict_suffix_sql()
        if on_conflict_extra_sql is None:
            on_conflict_extra_sql = ''

        # 拼接结果
        sql = f'''
        INSERT INTO {self.get_table_name()} ({fields_list}) 
        VALUES ({value_list})
        {on_conflict_extra_sql};
        '''
        return sql

    def get_on_conflict_suffix_sql(self):
        """获取冲突时添加在 insert 语句后的 sql"""
        sql = f"""
        ON CONFLICT({self.get_conflict_key()}) DO UPDATE SET
        crawled_times={self.get_table_name()}.crawled_times+1,
        {self.generate_update_info()}
        """
        return sql

    def get_conflict_key(self):
        """判断插入冲突的 key"""
        return self.get_primary_key()

    def generate_delete_sql(self):
        """生成删除语句"""
        k = self.get_primary_key()
        v = self.get_formatted_value(k)
        if not v:
            # 用于格式化
            v = '%s'
        return f'DELETE FROM {self.get_table_name()} WHERE {k}={v}'

    def generate_update_sql(self):
        """生成更新语句"""
        k = self.get_update_key()
        v = self.get_formatted_value(k)
        return f'UPDATE {self.get_table_name()} SET \n{self.generate_update_info()}' \
            f'\n WHERE {k}={v}'

    def get_update_key(self):
        """更新时使用的 key"""
        return self.get_conflict_key()

    def generate_update_info(self):
        """生成更新用的 key value

        用于更新和冲突时，更新不为空的内容
        """
        key_value_list = []
        for k in self.fields.keys():
            # 主键和创建时间
            if k == self.get_primary_key():
                continue
            if k == 'create_time_int4':
                continue
            v = self[k]
            if not v:
                continue
            name, _type = self.parse_name_type(k)
            key_value_list.append(f'{name}={self.get_formatted_value(k)}')
        return ',\n'.join(key_value_list)

    def generate_get_sql(self):
        """生成 get 语句"""
        return f'SELECT * FROM {self.get_table_name()}'

    def parse_param(self, data: Dict, key, default):
        v = None
        if key in data.keys():
            v = data[key]

        if not v:
            v = default
        return v

    def generate_select_sql(self, **params):
        """生成 select 语句"""
        fields = self.parse_param(params, 'fields', '*')
        where = self.parse_param(params, 'where', '')
        order = self.parse_param(params, 'order', '')
        desc = self.parse_param(params, 'desc', False)
        limit = self.parse_param(params, 'limit', 0)
        offset = self.parse_param(params, 'offset', 0)
        if where:
            if not where.startswith('WHERE'):
                where = f'WHERE {where}'
        if order:
            if not order.startswith('ORDER'):
                order = f'ORDER BY {order}'
            order += ' ' + ('ASC' if not desc else 'DESC')

        if limit:
            limit = f' LIMIT {limit}'
            if offset:
                limit += f' OFFSET {offset}'
        else:
            limit = ''
        return f"""
SELECT {fields} FROM {self.get_table_name()}
{where}
{order}
{limit}
"""


class BaseItemTest(unittest.TestCase):
    """Item 测试基类

    因为子类经常只重写少数方法，测试类也与其 item 类在一个文件中，所以基类也放在一个文件中，方便 import
    """
    item: BaseItem = BaseItem()
    """用于测试的 item"""

    def print_divider(self):
        print('\n\n' + '-' * 20)

    def test_sql(self):
        self.print_divider()
        print('sql')

    def test_default_value(self):
        self.print_divider()
        print('default_value')
        print(self.item)

    def test_generate_create_table_sql(self):
        self.print_divider()
        print('create_table')
        print(self.item.generate_create_table_sql())

    def test_generate_insert_sql(self):
        self.print_divider()
        print('insert')
        print(self.item.generate_insert_sql())

    def test_generate_delete_sql(self):
        self.print_divider()
        print('delete')
        print(self.item.generate_delete_sql())
        self.item[self.item.get_primary_key()] = 22
        print(self.item.generate_delete_sql())

    def test_generate_update_sql(self):
        self.print_divider()
        print('update')
        print(self.item.generate_update_sql())

    def test_generate_get_sql(self):
        self.print_divider()
        print(f'get')
        print(self.item.generate_get_sql())
