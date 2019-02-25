import inspect
from typing import List

from tool.android.android_studio_translator import FieldsHelper


class BaseModel():
    """基本数据模型
    peewee 也挺好的，有时间可以学习一下
    之前是在 scrapy 中实现了 BaseItem，这次也需要数据库，所以修改一下"""
    id = 0
    """
    主键
    第一行放类型，第二行放注释，后面的行忽略，如果只有一行则视为注释，类型默认为 TEXT
    要注意创建表、插入语句要对主键进行过滤"""

    create_time = ''
    """
    创建时间
    因为数据库保存为 TIMESTAMP，所以声明为 str，插入时需要格式化为字段"""

    update_time = ''
    """更新时间"""

    def __init__(self):
        """创建并解析"""
        self.fields_helper = FieldsHelper(self)
        """持有时注意过滤"""
        for k, v in self.fields_helper.fields_dict.items():
            if k not in self.__dict__.keys():
                # 不包启 k
                self.__dict__[k] = v.default_value

    # 建表相关的方法

    def get_table_name_pre(self):
        """表前缀
        之前的 discuz 表前缀默认为 pre，统一"""
        return 'pre_'

    def get_table_name(self):
        """获取表名"""
        return self.get_table_name_pre() + self.fields_helper.camel_to_under_line(self.__class__.__name__)

    def get_primary_key(self):
        """返回主键"""
        return 'id'

    def get_insert_ignore_keys(self):
        """插入时忽略的 key"""
        return [
            self.get_primary_key(),
            'field_helper',
            'create_time',
            'update_time',
        ]

    def get_head_fields(self):
        """建表时提前的字段
        scrapy 的 item 的字段将会按字母顺序排列，如果需要，则可以将其提前"""
        return []

    def get_tail_fields(self):
        """建表时放在最后的字段
        默认也会后解析 BaseModel ，这两个在最后的"""
        return [
            'create_time',
            'update_time',
        ]

    def get_on_conflict_suffix_sql(self):
        """获取冲突时添加在 insert 语句后的 sql"""
        return ''

    # 生成 sql 语句的相关方法

    def generate_create_table_sql(self):
        """
        生成建表的 SQL
        :return:
        """
        doc = inspect.getdoc(self)
        if doc:
            # 只取一行
            doc = doc.split('\n')[0]
        table_comment = '' if not doc else f"COMMENT='{doc}'"

        field_str = ''
        # 添加主键
        field_str += f"`{self.get_primary_key()}` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',\n"

        head_fields = self.get_head_fields()
        tail_fields = self.get_tail_fields()
        # 填充头部字段
        field_str = self.add_fields(field_str, head_fields)

        # 填充中间字段
        # 获取所有字段，这里没找到好的方法，这里不能用 __dict__，要用 __class__.__dict__，还要过滤方法
        for k in self.fields_helper.fields_dict.keys():
            if not self.is_valid_field_key(k):
                continue
            if not head_fields or k not in head_fields:
                if not tail_fields or k not in tail_fields:
                    field_str = self.add_fields_by_key(field_str, k)
        # 填充尾部字段
        field_str = self.add_fields(field_str, tail_fields)

        # 去掉最后的逗号
        field_str = field_str[:-2] + '\n'

        sql = f'CREATE TABLE IF NOT EXISTS `{self.get_table_name()}` (\n{field_str}){table_comment};'
        return sql

    def generate_insert_formatter_sql(self):
        """生成插入的 sql"""
        # 列出名字
        fields_list = []
        # 列出值，用 {} 包起来，后面用于格式化
        value_list = []
        for k, field in self.fields_helper.fields_dict.items():
            if not self.is_valid_field_key(k, True):
                continue
            # 字段名
            fields_list.append(field.name)
            # 值
            if isinstance(field.default_value, int):
                value_list.append("{%s}" % k)
            else:
                value_list.append("'{%s}'" % k)
        fields_list = ', '.join(fields_list)
        value_list = ', '.join(value_list)

        # 冲突处理
        on_conflict_extra_sql = self.get_on_conflict_suffix_sql()
        if on_conflict_extra_sql is None:
            on_conflict_extra_sql = ''

        sql = f'''
        INSERT INTO {self.get_table_name()}
        ({fields_list}) 
        VALUES ({value_list})
        {on_conflict_extra_sql};
        '''
        return sql

    def generate_insert_sql(self):
        """生成插入的 sql，用 self 的数据进行格式化"""
        return self.generate_insert_formatter_sql().format(**self.generate_insert_formatter_dict())

    def generate_insert_formatter_dict(self):
        """生成用于格式化的字典，对内容进行转义"""
        r = {}
        for k, v in self.__dict__.items():
            if not self.is_valid_field_key(k, True):
                # 格式化的字典，本可以按 key value 进行处理，这里可以不用过滤，但为了可能用于其他用途，保持统一
                continue
            if isinstance(v, str):
                # 替换单引号
                v = v.replace("'", "\\'")
                # 替换斜杠
                v = v.replace('\\', '\\\\')
                r[k] = v
            else:
                r[k] = v
        return r

    def is_valid_field_key(self, key, ignore_insert_keys=False):
        """
        是否是有效的字段 key
        :param key:
        :param ignore_insert_keys: 是否忽略插入时的部分 key
        :return:
        """
        if key.startswith('_') or key == self.get_primary_key():
            return False
        if ignore_insert_keys:
            if key in self.get_insert_ignore_keys():
                return False
        return True

    def add_fields(self, fields_str, fields_list: List[str]):
        """添加一个列表的各字段"""
        if not fields_list:
            return fields_str
        for k in fields_list:
            if not self.is_valid_field_key(k):
                continue
            fields_str = self.add_fields_by_key(fields_str, k)
        return fields_str

    def add_fields_by_key(self, fields_str, key):
        field = self.fields_helper.fields_dict.get(key)
        if field is None:
            raise KeyError(f'key:{key} not exists in {self}')
        # 拼上换行
        extra = '' if not field.extra else f' {field.extra}'
        comment = '' if not field.comment else f" COMMENT '{field.comment}'"
        fields_str += f'`{field.name}` {field.type}{extra}{comment},\n'
        return fields_str

    def generate_delete_sql(self):
        """生成删除语句"""
        primary_key = self.__dict__[self.get_primary_key()]
        if not primary_key:
            # 用于格式化
            primary_key = '%s'
        return f'DELETE FROM {self.get_table_name()} WHERE {self.get_primary_key()}={primary_key}'

    def generate_select_sql(self, condition: str = None, asc=True):
        """生成选择语句"""
        if not condition:
            if not condition.upper().startswith('WHERE'):
                condition = 'WHERE ' + condition
        return f"""
        SELECT * FROM {self.get_table_name()} {condition}
        ORDER BY {self.get_primary_key()} {'ASC' if asc else 'DESC'}
        """

    def __str__(self):
        return '{' + ','.join([f'{k}={v}' for k, v in self.__dict__.items()]) + '}'

    def __repr__(self):
        return self.__str__()
