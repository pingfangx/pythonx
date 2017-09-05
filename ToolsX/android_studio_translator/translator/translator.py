from xx import iox
from xx import filex
from xx import netx
from android_studio_translator.tools import Tools
import os
import math
import re
from xml.etree import ElementTree as Et


class Translator:
    """翻译全部文件"""

    def main(self):
        en_dir = r'C:\Users\Admin\Desktop\汉化\汉化包'
        cn_dir = en_dir
        dict_file = 'data/dict.txt'

        need_translation_dir = r'C:\Users\Admin\Desktop\汉化\android studio\resources_en\messages'
        need_translation_result_dir = 'data/need_translation'

        all_dict_file = r'data/all_dict.txt'
        omegat_dict_file = r'D:\workspace\TranslatorX\AndroidStudio\omegat\project_save.tmx'

        omegat_result_dict_file = 'data/omega_dict.tmx.xml'

        action_list = [
            ['退出', exit],
            ['检查key相同时，value是否有不一致', self.check_same_key_difference_value, en_dir],
            ['检查文件夹中的翻译是否完整', self.check_translation_complete, en_dir, cn_dir],
            ['检查英文相同时，翻译是否有不一致', self.check_same_en_difference_cn, en_dir, cn_dir, True],
            ['检查中英文件，并输出字典', self.get_all_translation, en_dir, cn_dir, dict_file],
            ['检查文件夹,生成需要翻译的多个文件', self.generate_need_translation_file, need_translation_dir,
             need_translation_result_dir],
            ['检查文件夹,生成需要翻译的单个文件', self.generate_need_translation_file2, need_translation_dir,
             need_translation_result_dir + '.properties'],
            ['使用字典更新OmegaT的记忆文件', self.update_omegat_dict, all_dict_file, omegat_dict_file, omegat_result_dict_file]
        ]
        iox.choose_action(action_list)

    @staticmethod
    def check_same_key_difference_value(dir_path):
        """如果key相同，value是否有不一致
        发现确实有不一致，所以必须区分文件"""

        file_list = Tools.list_file(dir_path)
        all_translation = dict()
        for file in file_list:
            print('\ncheck ' + file)
            translation_dict = Tools.get_dict_from_file(file, delete_value_and_symbol=True, trans_unicode=True)
            if all_translation:
                # 不为空再处理，为空的第一次直接update
                for key, value in translation_dict.items():
                    if key in all_translation.keys():
                        if all_translation[key] != value:
                            print('key相同%s，但value不一致\n%s\n%s' % (key, all_translation[key], value))
            all_translation.update(translation_dict)
            # print('the translation size is :%d' % len(sorted(all_translation.keys())))

    @staticmethod
    def check_same_en_difference_cn(en_dir, cn_dir, print_msg=False):
        """英文相同时，是否有不一致的翻译"""

        all_translation = dict()
        diff_translation = dict()
        en_file_list = Tools.list_file(en_dir)
        for en_file in en_file_list:
            print('\ncheck ' + en_file)
            cn_file = Translator.get_cn_file_name(en_dir, cn_dir, en_file)
            if not os.path.exists(cn_file):
                print('中文文件不存在' + cn_file)
                continue
            en_dict = Tools.get_dict_from_file(en_file)
            cn_dict = Tools.get_dict_from_file(cn_file, delete_cn_shortcut=True, trans_unicode=True)
            for key, en_value in en_dict.items():
                if key in cn_dict.keys():
                    # 有key对应的中英文
                    cn_value = cn_dict[key]
                    if cn_value != en_value:
                        # 中英文不一样才算翻译
                        if en_value in all_translation.keys():
                            pre_translation = all_translation[en_value]
                            if pre_translation != cn_value:
                                if en_value not in diff_translation.keys():
                                    diff_translation[en_value] = pre_translation + '\n' + cn_value
                                else:
                                    pre_diff_translation = diff_translation[en_value]
                                    if cn_value not in pre_diff_translation.split('\n'):
                                        # 之前没有记录过才再记录
                                        diff_translation[en_value] = pre_diff_translation + '\n' + cn_value
                                if print_msg:
                                    print('\n字典中已经存在%s，但翻译不相同\n%s\n%s' % (en_value, pre_translation, cn_value))
                        else:
                            all_translation[en_value] = cn_value
            if print_msg:
                print('the size is %d' % len(sorted(all_translation.keys())))
        # 读取守毕
        for key in diff_translation.keys():
            all_translation.pop(key)
        return all_translation, diff_translation

    @staticmethod
    def check_translation_complete(en_dir, cn_dir):
        """翻译是否完整"""
        en_file_list = Tools.list_file(en_dir)
        not_complete_file = []
        miss_file = []
        for en_file in en_file_list:
            print('\ncheck ' + en_file)
            cn_file = Translator.get_cn_file_name(en_dir, cn_dir, en_file)
            if not os.path.exists(cn_file):
                print('中文文件不存在' + cn_file)
                miss_file.append(cn_file)
                continue
            en_dict = Tools.get_dict_from_file(en_file)
            cn_dict = Tools.get_dict_from_file(cn_file, trans_unicode=True)
            is_complete = True
            for key, en_value in en_dict.items():
                if key not in cn_dict.keys():
                    is_complete = False
                    print('没有翻译%s对应的%s' % (key, en_value))
                else:
                    cn_value = cn_dict[key]
                    if en_value == cn_value:
                        is_complete = False
                    print('%s对应的翻译仍然是%s，未翻译' % (key, en_value))
            if not is_complete:
                print('文件未完全翻译' + en_file)
                not_complete_file.append(en_file)
        print('缺少%d个文件' % len(miss_file))
        print('有%d个文件未翻译完整' % len(not_complete_file))

    @staticmethod
    def get_cn_file_name(en_dir, cn_dir, en_file):
        """获取英文文件对应的中文文件，可能会变，所以提出来"""
        cn_file = en_file.replace(en_dir, cn_dir)
        cn_file = filex.get_result_file_name(cn_file, '_zh_CN')
        return cn_file

    @staticmethod
    def get_all_translation(en_dir, cn_dir, dict_file, dict_diff_file=None):
        if dict_diff_file is None:
            dict_diff_file = filex.get_result_file_name(dict_file, '_diff')
        """读取并输出所有翻译"""
        all_translation, diff_translation = Translator.check_same_en_difference_cn(en_dir, cn_dir)
        result = list()
        for key, value in all_translation.items():
            result.append('%s=%s\n' % (key, value))
        print('size is %d' % len(sorted(all_translation.keys())))
        filex.write_lines(dict_file, result)

        result = list()
        for key, value in diff_translation.items():
            result.append('%s=%s\n\n' % (key, value))
        print('size is %d' % len(sorted(diff_translation.keys())))
        filex.write_lines(dict_diff_file, result)

    @staticmethod
    def generate_need_translation_file(en_dir, result_dir):
        """生成需要翻译的文件"""
        en_file_list = Tools.list_file(en_dir)
        all_translation = dict()
        for en_file in en_file_list:
            en_dict = Tools.get_dict_from_file(en_file)
            all_translation.update(en_dict)

        i = 0
        size = 3000
        result = list()
        for key, value in all_translation.items():
            i += 1
            result.append('%s=%s\n' % (key, value))
            if i % size == size - 1:
                index = int(i / size)
                result_file = '%s\\%2d.properties' % (result_dir, index)
                filex.write_lines(result_file, result)
                result.clear()
        if result:
            index = int(i / size)
            result_file = '%s\\%2d.properties' % (result_dir, index)
            filex.write_lines(result_file, result)
            result.clear()

    @staticmethod
    def generate_need_translation_file2(en_dir, result_file):
        """生成需要翻译的文件"""
        en_file_list = Tools.list_file(en_dir)
        all_translation = dict()
        for en_file in en_file_list:
            en_dict = Tools.get_dict_from_file(en_file)
            all_translation.update(en_dict)

        result = list()
        for key, value in all_translation.items():
            result.append('%s=%s\n' % (key, value))
        filex.write_lines(result_file, result)

    @staticmethod
    def update_omegat_dict(dict_file, omegat_dict_file, result_dict_file):
        """更新omegat的记忆文件"""

        pre_dict = Tools.get_dict_from_file(dict_file)
        print('pre size is %d' % len(sorted(pre_dict.keys())))
        omegat_dict = Translator.get_omegat_dict(omegat_dict_file)
        print('omegat size is %d' % len(sorted(omegat_dict.keys())))

        # 更新，以omegat为准
        pre_dict.update(omegat_dict)

        print('result size is %d' % len(sorted(pre_dict.keys())))
        Tools.save_omegat_dict(pre_dict, result_dict_file)

    @staticmethod
    def get_omegat_dict(file_path):
        """读取omegat的记忆文件"""
        tree = Et.parse(file_path)
        tmx = tree.getroot()
        body = tmx.find('body')
        result = dict()
        for tu in body.iter('tu'):
            cn = None
            en = None
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'EN-US':
                    en = tuv.find('seg').text
                    # 转换一下
                    if en:
                        en = re.sub(r'&(\w)', '', en)
                elif tuv.attrib['lang'] == 'ZH-CN':
                    cn = tuv.find('seg').text
            if cn and en:
                result[en] = cn
        return result


if __name__ == '__main__':
    Translator().main()
