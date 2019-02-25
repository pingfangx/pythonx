import filecmp
import os
import re
from xml.etree import ElementTree as Et

from tool.android.android_studio_translator.tools import Tools
from xx import filex
from xx import iox


class Translator:
    """翻译全部文件"""

    def main(self):

        en_dir = r'D:\workspace\TranslatorX\AndroidStudio\source\2.3.3\lib\resources_en'
        cn_dir = r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\4'
        dict_file = 'data/dict.txt'

        need_translation_dir = r'C:\Users\Admin\Desktop\汉化\android studio\resources_en\messages'
        need_translation_result_dir = 'data/need_translation'

        all_dict_file = r'data/all_dict.txt'
        omegat_dict_file = r'data/project_save.tmx'

        omegat_result_dict_file = 'data/omega_dict.tmx.xml'

        source_dir = r'D:\workspace\TranslatorX\AndroidStudio\source\AndroidStudio\resources_en\messages'
        target_dir = r'D:\workspace\TranslatorX\AndroidStudio\target\AndroidStudio\resources_en\messages'

        incomplete_file = 'data/incomplete.properties'
        compare_dirs = [
            r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\整理',
            r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\2',
            r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\3',
            r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\1',
            r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\4',
        ]
        phone_translation_dir = [r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\phone']
        action_list = [
            ['退出', exit],
            ['检查key相同时，value是否有不一致', self.check_same_key_difference_value, en_dir],
            ['检查文件夹中的翻译是否完整', self.check_translation_complete, en_dir, cn_dir, None, ''],
            ['检查英文相同时，翻译是否有不一致', self.check_same_en_difference_cn, en_dir, cn_dir, True],
            ['检查中英文件，并输出词典', self.get_all_translation, en_dir, cn_dir, None, None, ''],
            ['检查文件夹,生成需要翻译的多个文件', self.generate_need_translation_file, need_translation_dir,
             need_translation_result_dir],
            ['检查文件夹,生成需要翻译的单个文件', self.generate_need_translation_file2, need_translation_dir,
             need_translation_result_dir + '.properties'],
            ['使用词典更新OmegaT的记忆文件', self.update_omegat_dict, all_dict_file, omegat_dict_file, omegat_result_dict_file],
            ['检查输出目录是否翻译完整' + target_dir, self.check_translation_complete, source_dir, target_dir, incomplete_file],
            ['比较几个文件夹的翻译结果并输出词典（可备选）', self.compare_translation, en_dir, compare_dirs, omegat_dict_file],
            ['比较几个文件夹的翻译结果并输出词典（以文件顺序为优先级单个结果）', self.compare_translation_by_index, en_dir, compare_dirs],
            ['比较手机翻译结果并输出OmegaT词典(不转unicode)', self.compare_translation, en_dir, phone_translation_dir, None,
             r'data/phone_dict.tmx.xml', None, False, False],
            ['将%s导出为OmegaT记忆库' % all_dict_file, self.export_to_omegat, all_dict_file],
            ['将OmegaT的词库导出为文本', self.export_omegat_dictionary_to_file,
             r'D:\workspace\TranslatorX\AndroidStudio\tm\99all_dict.tmx']
        ]
        iox.choose_action(action_list)

    @staticmethod
    def check_same_key_difference_value(dir_path):
        """如果key相同，value是否有不一致
        发现确实有不一致，所以必须区分文件"""

        file_list = filex.list_file(dir_path)
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
    def check_same_en_difference_cn(en_dir, cn_dir, print_msg=False, suffix='', trans_unicode=True):
        """英文相同时，是否有不一致的翻译"""

        all_translation = dict()
        diff_translation = dict()
        en_file_list = filex.list_file(en_dir, '\.(?!png|gif)')
        for en_file in en_file_list:
            print('\ncheck ' + en_file)
            cn_file = Translator.get_cn_file_name(en_dir, cn_dir, en_file, suffix)
            if not os.path.exists(cn_file):
                print('中文文件不存在' + cn_file)
                continue
            en_dict = Tools.get_dict_from_file(en_file)
            cn_dict = Tools.get_dict_from_file(cn_file, delete_cn_shortcut=True, trans_unicode=trans_unicode)
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
                                    print('\n词典中已经存在%s，但翻译不相同\n%s\n%s' % (en_value, pre_translation, cn_value))
                        else:
                            all_translation[en_value] = cn_value
            if print_msg:
                print('the size is %d' % len(sorted(all_translation.keys())))
        # 读取守毕
        for key in diff_translation.keys():
            all_translation.pop(key)
        return all_translation, diff_translation

    @staticmethod
    def check_translation_complete(en_dir, cn_dir, out_put=None, suffix=''):
        """翻译是否完整"""
        incomplete_dict = dict()
        en_file_list = filex.list_file(en_dir, '\.(?!png|gif)')
        incomplete_file = []
        miss_file = []
        complete_count = 0
        same_file = []
        complete_file = []
        for en_file in en_file_list:
            # print('\ncheck ' + en_file)
            cn_file = Translator.get_cn_file_name(en_dir, cn_dir, en_file, suffix)
            if not os.path.exists(cn_file):
                # print('中文文件不存在' + cn_file)
                miss_file.append(cn_file)
                continue
            if filecmp.cmp(en_file, cn_file):
                # print('文件相同' + en_file)
                same_file.append(en_file)
                continue
            en_dict = Tools.get_dict_from_file(en_file)
            cn_dict = Tools.get_dict_from_file(cn_file, trans_unicode=True)
            is_complete = True
            translation_count_in_file = 0
            for key, en_value in en_dict.items():
                if key not in cn_dict.keys():
                    is_complete = False
                    incomplete_dict[key] = en_value
                    # print('没有翻译%s对应的%s' % (key, en_value))
                else:
                    cn_value = cn_dict[key]
                    if en_value == cn_value:
                        is_complete = False
                        incomplete_dict[key] = en_value
                        # print('%s对应的翻译仍然是%s，未翻译' % (key, en_value))
                    else:
                        translation_count_in_file += 1
                        complete_count += 1
            if not is_complete:
                print('文件未完全翻译' + en_file)
                incomplete_file.append(en_file)
            else:
                if translation_count_in_file == 0:
                    # 一句都没翻译
                    # print('文件一句都没翻译' + en_file)
                    same_file.append(en_file)
                else:
                    complete_file.append(en_file)
                    print('文件翻译完整' + en_file)
        print('缺少%d个文件' % len(miss_file))
        print(miss_file)
        print('有%d个文件完全相同' % len(same_file))
        print('有%d个文件未翻译完整' % len(incomplete_file))
        print(incomplete_file)
        print('有%d个文件完整翻译,共%d条翻译' % (len(complete_file), complete_count))
        if out_put is not None:
            result = list()
            for key, value in incomplete_dict.items():
                result.append('%s=%s\n\n' % (key, value))
            print('incomplete size is %d' % len(sorted(incomplete_dict.keys())))
            filex.write_lines(out_put, result)

    @staticmethod
    def get_cn_file_name(en_dir, cn_dir, en_file, suffix=None):
        """获取英文文件对应的中文文件，可能会变，所以提出来"""
        cn_file = en_file.replace(en_dir, cn_dir)
        cn_file = filex.get_result_file_name(cn_file, suffix)
        return cn_file

    @staticmethod
    def get_all_translation(en_dir, cn_dir, dict_file=None, dict_diff_file=None, suffix=''):
        if dict_file is None:
            base_name = os.path.split(cn_dir)[1]
            dict_file = 'data/%s_dict.txt' % base_name
        if dict_diff_file is None:
            dict_diff_file = filex.get_result_file_name(dict_file, '_diff')
        """读取并输出所有翻译"""
        all_translation, diff_translation = Translator.check_same_en_difference_cn(en_dir, cn_dir, False, suffix)

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
        en_file_list = filex.list_file(en_dir)
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
        en_file_list = filex.list_file(en_dir)
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

    @staticmethod
    def compare_translation_by_index(en_dir, compare_dir_list):
        """读取每个文件夹中的翻译 ，按优先组输出"""
        Translator.compare_translation(en_dir, compare_dir_list, by_index=True)

    @staticmethod
    def compare_translation(en_dir, compare_dir_list, omegat_dict_file=None, dict_file=None, dict_diff_file=None,
                            by_index=False, trans_unicode=True):
        if dict_file is None:
            dict_file = 'data/dict.txt'
        if dict_diff_file is None:
            dict_diff_file = filex.get_result_file_name(dict_file, '_diff')
        separator = '[xx|]'
        dict_list = list()
        for i in compare_dir_list:
            if i == r'C:\Users\Admin\Desktop\AndroidStudio汉化\汉化包\整理':
                t_dict = dict()
                for i_file in filex.list_file(i, '.properties'):
                    t_dict.update(filex.get_dict_from_file(i_file))
                dict_list.append(t_dict)
                continue
            i_all_translation, i_diff_translation = Translator.check_same_en_difference_cn(en_dir, i, False, '',
                                                                                           trans_unicode=trans_unicode)
            dict_list.append(i_all_translation)
        if omegat_dict_file is not None:
            dict_list.insert(0, Translator.get_omegat_dict(omegat_dict_file))

        for i in range(len(dict_list)):
            print('%d中共包含翻译%d条' % (i + 1, len(sorted(dict_list[i].keys()))))

        all_translation = dict()
        diff_translation = dict()
        print_i = True
        if by_index:
            # 按倒序更新，得到结果
            for i in range(len(dict_list) - 1, -1, -1):
                all_translation.update(dict_list[i])
                print('更新%d后，size是%d' % (i + 1, len(sorted(all_translation.keys()))))
        else:
            for i in range(len(dict_list)):
                i_dict = dict_list[i]
                index = 0
                length = len(sorted(i_dict.keys()))
                for key, i_value in i_dict.items():
                    index += 1
                    if print_i:
                        print('\n检查%d/%d,%s' % (index, length, key))
                        print('词典%d中是%s' % (i, i_value))
                    has_diff = False
                    for j in range(i + 1, len(dict_list)):
                        j_dict = dict_list[j]
                        if key in j_dict:
                            j_value = j_dict[key]
                            if i_value == j_value:
                                if print_i:
                                    print('词典%d中相同' % j)
                            else:
                                has_diff = True
                                if key in diff_translation.keys():
                                    pre_translation = diff_translation[key]
                                    if j_value not in pre_translation.split(separator):
                                        diff_translation[key] = pre_translation + separator + j_value.replace('\n', '')
                                else:
                                    diff_translation[key] = (i_value + separator + j_value).replace('\n', '')
                                if print_i:
                                    print('词典%d中是%s' % (j, j_value))
                            # 处理后移除
                            j_dict.pop(key)
                        else:
                            if print_i:
                                print('词典%d中缺少' % j)
                    if not has_diff:
                        if print_i:
                            print('统一翻译')
                        if i_value:
                            # 只添加不为空的
                            all_translation[key] = i_value
                print('%d中处理%d条，其中%d条翻译相同,%d条不同' % (
                    i, len(sorted(i_dict.keys())), len(sorted(all_translation.keys())),
                    len(sorted(diff_translation.keys()))))

        print('size is %d' % len(sorted(all_translation.keys())))
        if all_translation:
            if dict_file.endswith('.tmx') or dict_file.endswith('.tmx.xml'):
                Tools.save_omegat_dict(all_translation, dict_file)
            else:
                result = list()
                for key, value in all_translation.items():
                    result.append('%s=%s\n' % (key, value))
                filex.write_lines(dict_file, result)

        print('diff size is %d' % len(sorted(diff_translation.keys())))
        if diff_translation:
            result = list()
            for key, value in diff_translation.items():
                result.append('%s=%s\n' % (key, value))
            filex.write_lines(dict_diff_file, result)

    @staticmethod
    def export_to_omegat(file_path, result_file=None):
        """导出为OmegaT的记忆文件"""
        if result_file is None:
            result_file = filex.get_result_file_name(file_path, '', '.tmx.xml')
        translation_dict = filex.get_dict_from_file(file_path)
        output_dict = dict()
        for key, value in translation_dict.items():
            if value:
                if '【】' in value:
                    output_dict[key] = value.split('【】')[0]
                else:
                    output_dict[key] = value
        Tools.save_omegat_dict(output_dict, result_file)

    @staticmethod
    def export_omegat_dictionary_to_file(file_path, result_file=None):
        """导出omegat的词库为文件"""
        if result_file is None:
            result_file = filex.get_result_file_name(file_path, '', 'txt')
        omegat_dict = Translator.get_omegat_dict(file_path)

        result = list()
        for key, value in omegat_dict.items():
            result.append('%s=%s\n' % (key, value))
        print('size is %d' % len(sorted(omegat_dict.keys())))
        filex.write_lines(result_file, result)


if __name__ == '__main__':
    Translator().main()
