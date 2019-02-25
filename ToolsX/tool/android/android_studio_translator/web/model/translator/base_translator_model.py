from tool.android.android_studio_translator import BaseModel


class BaseTranslatorModel(BaseModel):
    """翻译相关的模型"""

    def get_table_name_pre(self):
        return 'xx_translator_'

    def generate_insert_formatter_dict(self):
        """处理字典"""
        r = super().generate_insert_formatter_dict()
        user_dict = {
            'pingfangx': ('平方X', 10001)
        }
        for k, v in r.items():
            if k.endswith('_user'):
                # 以 _user 结尾
                if v in user_dict.keys():
                    # 作者属于预设字典
                    # 替换用户名
                    r[k] = user_dict[v][0]
                    user_id_key = k.replace('_user', '_user_id')
                    if user_id_key in r.keys():
                        if r[user_id_key] == 0:
                            # 如果没有用户 id，取预设 id 进行设置
                            r[user_id_key] = user_dict[v][1]
        return r
