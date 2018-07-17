from android_studio_translator.web.model.base.base_model import BaseModel
from xx.database.mysql_helper import MySqlHelper


class MySqlModelHelper(MySqlHelper):
    def __init__(self, model):
        super().__init__()
        self.model: BaseModel = model

    def create_table(self):
        self.execute(self.model.generate_create_table_sql())
