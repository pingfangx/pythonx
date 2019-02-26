import configparser
import os
from typing import List


class TranslatorXConfig:
    """处理配置

    该类只负责读取、写入配置（不负责默认值的赋值，因为可能依赖其他类声明的常量）
    也就是外部不关心配置名
    该类也不 import 其他业务类
    """

    def __init__(self, config_file=''):
        self.config_file = config_file
        if not self.config_file:
            self.config_file = 'translatorx.cfg'
        if not os.path.exists(self.config_file):
            print(f'配置文件不存在 {self.config_file}')
            exit()
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file, encoding='utf-8')

    def get_software_home_path(self) -> str:
        return os.path.abspath(self.get_config('software_home_path'))

    def get_omegat_workspace(self) -> str:
        return os.path.abspath(self.get_config('omegat_workspace'))

    def get_software_name_list(self) -> List[str]:
        return self.get_list_config('software_name_list')

    def get_software_version_list(self) -> List[str]:
        return self.get_list_config('software_version_list')

    def get_translation_locale(self) -> str:
        return self.get_config('translation_locale')

    def get_list_config(self, key) -> List[str]:
        config = self.get_config(key)
        if config:
            return [i for i in config.split('\n') if i]
        return []

    def get_config(self, key) -> str:
        section_name = 'translatorx'
        if self.config.has_section(section_name):
            section = self.config[section_name]
            if section and key in section:
                return section[key]
        return ''
