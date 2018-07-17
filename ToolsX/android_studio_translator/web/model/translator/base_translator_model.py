from android_studio_translator.web.model.base.base_model import BaseModel


class BaseTranslatorModel(BaseModel):
    """翻译相关的模型"""

    def get_table_name_pre(self):
        return 'xx_translator_'
