import datetime
import os
import re
from xml.etree import ElementTree as Et

from tool.android.android_studio_translator.delete_action import DeleteAction
from xx import encodex
from xx import filex
from xx import iox


class Tools:
    """
    翻译相关的方法集
    相关文单：[AndroidStudio翻译(1)-总述](http://blog.pingfangx.com/2353.html)
    """

    def main(self):
        en_file = 'actions_bundle/data/ActionsBundle_en.properties'
        """原文件"""

        en_add_file = 'actions_bundle/data/ActionsBundle_en_add.properties'
        """补充过的英文文件"""

        unicode_file = 'actions_bundle/data/ActionsBundle_unicode.properties'
        """汉化文件"""

        cn_file = 'actions_bundle/data/ActionsBundle_cn.properties'
        """转为中文"""

        cn_modified_file = 'actions_bundle/data/ActionsBundle_cn_modified.properties'
        """中文修改过的文件，删除快捷方式，删除末尾的.或省略号"""

        omega_tmx_file = 'actions_bundle/data/project_save.tmx.xml'
        omega_saved_file = r"D:\workspace\TranslatorX\AndroidStudio\omegat\project_save.tmx"
        action_list = [
            ['退出', exit],
            ['参照翻译(未翻译保留)', self.translate_file_by_reference, en_file, cn_modified_file],
            ['参照翻译(未翻译标记)', self.translate_file_by_reference, en_file, cn_modified_file, None, '%s=%s【未翻译】'],
            ['将文件的unicode转为中文', self.change_unicode_to_chinese, unicode_file],
            ['将文件的中文转为unicode', self.change_chinese_to_unicode, cn_file],
            ['将中文翻译结果导出为OmegaT数据（可用于检查换行）', self.convert_to_omegat_dict, en_file, cn_modified_file, omega_tmx_file],
        ]
        for delete_action in DeleteAction.action_list:
            action_list.append(
                ['删除文件中的%s' % delete_action[1], DeleteAction.delete_symbol, delete_action[0], en_add_file])
        for delete_action in DeleteAction.action_list:
            action_list.append(
                ['删除OmegaT文件中的%s' % delete_action[1], DeleteAction.delete_symbol, delete_action[0], omega_saved_file,
                 DeleteAction.FILE_TYPE_FILE])

        iox.choose_action(action_list)

    def translate_file_by_reference(self, en_file, cn_file, result_file=None, untranslated_replace=None):
        """
        根据参考翻译文件
        :param en_file:英文
        :param cn_file: 参考中文
        :param result_file: 结果文件
        :param untranslated_replace:未翻译时替换
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(en_file, '_translation_result')

        translation_dict = Tools.get_dict_from_file(cn_file)
        result = self.translate_file_by_dict(en_file, translation_dict, untranslated_replace)

        filex.write_lines(result_file, result)

    @staticmethod
    def translate_file_by_dict(file_path, translation_dict, untranslated_replace=None):
        """
        翻译文件
        :param file_path: 要翻译的文件
        :param translation_dict: 字典
        :param untranslated_replace: 未翻译的用什么替换，（将会执行untranslated % (key_value[0], key_value[1])），
        如果执行失败则直接用其值替换
        默认为None，如果为None表示不替换
        :return:
        """
        lines = filex.read_lines(file_path)
        if lines is None:
            return None

        result = []
        untranslated_count = 0
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                # 翻译
                key = key_value[0]
                if key in translation_dict.keys():
                    translation = translation_dict[key]
                    if translation is not None and translation != '':
                        line = '%s=%s' % (key_value[0], translation)
                else:
                    # line += '待翻译'
                    untranslated_count += 1
                    print('%d-%s-未翻译' % (untranslated_count, line))
                    if untranslated_replace is not None:
                        try:
                            line = untranslated_replace % (key_value[0], key_value[1])
                        except TypeError:
                            line = untranslated_replace
            result.append(line + '\n')
        return result

    @staticmethod
    def change_unicode_to_chinese(file_path, output_file=None):
        """
        将unicode转为中文
        :param file_path:源文件
        :param output_file: 输出文件
        :return:
        """
        if output_file is None:
            output_file = filex.get_result_file_name(file_path, '_cn_result')

        lines = filex.read_lines(file_path)
        if lines is None:
            return

        result = []
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                line = '%s=%s' % (key_value[0], encodex.unicode_str_to_chinese(key_value[1]))
            result.append(line + '\n')
        filex.write_lines(output_file, result)

    @staticmethod
    def change_chinese_to_unicode(file_path, output_file=None):
        """
        将中文转为unicode
        :param file_path:
        :param output_file:
        :return:
        """
        if output_file is None:
            output_file = filex.get_result_file_name(file_path, '_unicode_result')

        lines = filex.read_lines(file_path)
        if lines is None:
            return

        result = []
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                line = '%s=%s' % (key_value[0], encodex.chinese_to_unicode(key_value[1]))
            result.append(line + '\n')
        filex.write_lines(output_file, result)

    @staticmethod
    def convert_to_omegat_dict(en_file, cn_file, output_file=None):
        """
        将翻译结果转为omegaT的字典
        :param en_file: 英文文件
        :param cn_file: 中文文件
        :param output_file: 输出文件
        :return:
        """
        if output_file is None:
            output_file = filex.get_result_file_name(cn_file, '_omegat_result', 'xml')

        en_dict = Tools.get_dict_from_file(en_file)
        cn_dict = Tools.get_dict_from_file(cn_file)

        tmx = Et.Element('tmx')
        tmx.attrib['version'] = '1.1'
        Et.SubElement(tmx, 'header')
        body = Et.SubElement(tmx, 'body')
        for (k, v) in cn_dict.items():
            if k in en_dict.keys():
                en_value = en_dict[k]
                cn_value = v
                # 判断是否有多个句子，"."加一个空格
                added = False
                if '. ' in en_value:
                    en_split = en_value.split('. ')
                    if en_split[1] != '':
                        # 包含“.”，不是在最后的“...”
                        # 检查中文
                        if '。 ' in cn_value:
                            cn_split = cn_value.split('。 ')
                            if len(en_split) == len(cn_split):
                                added = True
                                # 中英长度相等
                                for i in range(len(en_split)):
                                    Tools.add_translate_element(body, en_split[i], cn_split[i])
                                    print('分开添加:' + cn_split[i])
                            else:
                                print('')
                                print(en_value)
                                print(cn_value)
                                print('%d,%d' % (len(en_split), len(cn_split)))
                        else:
                            print('')
                            print(en_value)
                            print(cn_value)
                            print('英文中有“. ”，中文中不包含“。 ”')
                if not added:
                    if cn_value:
                        # 只添加不为空的
                        Tools.add_translate_element(body, en_value, cn_value)

        tree = Et.ElementTree(tmx)
        tree.write(output_file, encoding='utf-8')
        print('输出为' + output_file)

    @staticmethod
    def save_omegat_dict(omega_dict, output_file):
        """保存
        """
        tmx = Et.Element('tmx')
        tmx.attrib['version'] = '1.1'
        Et.SubElement(tmx, 'header')
        body = Et.SubElement(tmx, 'body')
        for (k, v) in omega_dict.items():
            if v:
                # 只添加不为空的
                Tools.add_translate_element(body, k, v)

        tree = Et.ElementTree(tmx)
        tree.write(output_file, encoding='utf-8')
        print('输出为' + output_file)

    @staticmethod
    def add_translate_element(element, en, cn):
        """
        向element中添加一个翻译
        :param element:
        :param en
        :param cn
        :return:
        """

        tu = Et.SubElement(element, 'tu')
        # 英文
        tuv = Et.SubElement(tu, 'tuv')
        tuv.attrib['lang'] = 'EN-US'
        seg = Et.SubElement(tuv, 'seg')
        seg.text = en
        # 中文
        # TODO 这里需要从原文件中读取 tu 及 tuv ，修改或添加时间作者后再写入
        tuv2 = Et.SubElement(tu, 'tuv')
        tuv2.attrib['lang'] = 'ZH-CN'
        tuv2.attrib['changeid'] = 'pingfangx'
        # 注意时区 utc
        tuv2.attrib['changedate'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        tuv2.attrib['creationid'] = 'pingfangx'
        tuv2.attrib['creationdate'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        seg2 = Et.SubElement(tuv2, 'seg')
        seg2.text = cn

    @staticmethod
    def get_dict_from_file(file_path, separator='=', delete_value_ellipsis=True, delete_value_underline=True,
                           delete_value_and_symbol=False, delete_cn_shortcut=False, trans_unicode=False):
        """
        从文件中读取字典，
        :param file_path:文件路径
        :param separator:分隔符
        :return: 如果有错返回None
        :param delete_value_ellipsis:删除省略号
        :param delete_value_underline: 删除快捷方式
        :param delete_value_and_symbol: 是否删降&符号
        :param delete_cn_shortcut: 是否删除中文翻译中的快捷方式
        :param trans_unicode: 将unicode转为中文
        """
        result = filex.get_dict_from_file(file_path, separator)
        if result is None:
            return None

        if delete_value_ellipsis or delete_value_underline or trans_unicode:
            # (空白?点一次或多次)
            p_ellipsis = r'(\s?\.+)$'
            # 空白?，左括号，&?，字母，右括号
            p_shortcut = r'\s?\(&?\w\)$'
            # &后跟一字母
            p_add_symbol = r'&(\w)'
            for key, value in result.items():
                if delete_value_ellipsis:
                    value = re.sub(p_ellipsis, '', value)
                if delete_value_underline:
                    value = value.replace('_', '')
                if delete_value_and_symbol:
                    value = re.sub(p_add_symbol, r'\1', value)
                if delete_cn_shortcut:
                    value = re.sub(p_shortcut, '', value)
                if trans_unicode:
                    value = encodex.unicode_str_to_chinese(value)
                result[key] = value
        return result

    @staticmethod
    def get_dict_from_omegat(file_path):
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
                elif tuv.attrib['lang'] == 'ZH-CN':
                    cn = tuv.find('seg').text
            if en is not None:
                # 中文允许为空
                result[en] = cn
        return result

    @staticmethod
    def list_file(dir_path, name_pattern=None):
        """
        获取目录中的文件，组成以文件名（不带后缀的）为key的字典
        :param dir_path:
        :param name_pattern: 文件名的正则匹配
        :return:
        """
        file_list = list()
        for parent, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                if name_pattern is not None:
                    if re.search(name_pattern, file) is not None:
                        file_list.append(parent + '\\' + file)
                else:
                    file_list.append(parent + '\\' + file)
        return file_list


if __name__ == '__main__':
    Tools().main()
