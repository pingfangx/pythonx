import os
import re
import shutil
from xml.etree import ElementTree as Et

from android_studio_translator.keymap_default.keymap_default import KeymapDefault
from android_studio_translator.tools import Tools
from xx import filex
from xx import iox


class Tips:
    """
    AndroidStudio的每日提示文件
    [AndroidStudio翻译(6)-Tip of the Day每日提示中文翻译](http://blog.pingfangx.com/2358.html)
    """
    RESULT_TYPE_ANDROID_STUDIO = 0
    RESULT_TYPE_GITHUB_PAGES = 1

    VARIABLE_DICT = {
        'productName': 'AndroidStudio',
        'majorVersion': '3',
        'minorVersion': '0',
    }

    KEYMAP_CN_DICT = KeymapDefault.get_keymap_dict_from_file('../keymap_default/data/keymap_default.xml')
    KEYMAP_CN_DICT.update(KeymapDefault.get_keymap_dict_from_file('data/keymap_add.xml'))
    KEYMAP_EN_DICT = KeymapDefault.get_keymap_dict_from_file('../keymap_default/data/keymap_default.xml', False)
    KEYMAP_EN_DICT.update(KeymapDefault.get_keymap_dict_from_file('data/keymap_add.xml', False))

    KEYMAP_DICT = KEYMAP_CN_DICT

    github_pages_action_list = list()

    def main(self):
        tips_en_dir = r'D:\workspace\TranslatorX\AndroidStudio\source\tips'
        # 翻译结果目录
        tips_cn_dir = r'D:\workspace\TranslatorX\AndroidStudio\target\2.3.3\lib\resources_en\tips'
        # 处理为AndroidStudio的目录
        tips_android_studio_dir = tips_cn_dir + r'_android_studio'
        # 处理为github page的目录
        tips_github_pages_en_dir = r'D:\workspace\github.pingfangx.io\android_studio\tips' + r'\en'
        tips_github_pages_cn_dir = r'D:\workspace\github.pingfangx.io\android_studio\tips' + r'\cn'

        # 清单文件
        tips_manifest_file = r'D:\workspace\TranslatorX\AndroidStudio\source\AndroidStudio\resources\META-INF' \
                             r'\IdeTipsAndTricks.xml '
        tips_manifest_translation_file = r'D:\workspace\TranslatorX\AndroidStudio\target\IdeTipsAndTricks_name_zh_CN' \
                                         r'.properties '

        # 文件名翻译结果
        tips_names_cn_file = 'data/IdeTipsAndTricks_name_zh_CN_cn_result.properties'

        Tips.github_pages_action_list = [
            [tips_names_cn_file, tips_en_dir, tips_github_pages_en_dir, 0, 'en'],
            [tips_names_cn_file, tips_en_dir, tips_github_pages_en_dir, 1, 'en'],
            [tips_names_cn_file, tips_cn_dir, tips_github_pages_cn_dir, 0, 'cn'],
            [tips_names_cn_file, tips_cn_dir, tips_github_pages_cn_dir, 1, 'cn'],
        ]
        action_list = [
            ['退出', exit],
            ['处理清单文件，整理tips的名称方便翻译', self.process_tips_manifest_file, tips_manifest_file],
            ['将翻译结果的unicode转为中文件', Tools.change_unicode_to_chinese, tips_manifest_translation_file],
            ['处理tips翻译结果为AndroidStudio用', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir,
             Tips.RESULT_TYPE_ANDROID_STUDIO, tips_android_studio_dir],
            ['处理所有GitHub Pages文件', self.process_all_github_pages],
            ['处理tips原文为GitHub Pages用（数字命名）', self.process_tips_translation_result, tips_names_cn_file, tips_en_dir,
             Tips.RESULT_TYPE_GITHUB_PAGES, tips_github_pages_en_dir, 0, 'en'],
            ['处理tips原文为GitHub Pages用（数字加名字命名）', self.process_tips_translation_result, tips_names_cn_file, tips_en_dir,
             Tips.RESULT_TYPE_GITHUB_PAGES, tips_github_pages_en_dir, 1, 'en'],
            ['处理tips翻译结果为GitHub Pages用（数字命名）', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir,
             Tips.RESULT_TYPE_GITHUB_PAGES, tips_github_pages_cn_dir],
            ['处理tips翻译结果为GitHub Pages用（数字加名字命名）', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir,
             Tips.RESULT_TYPE_GITHUB_PAGES, tips_github_pages_cn_dir, 1],
            ['将目录中的tips按顺序排序', self.order_tips_file, tips_names_cn_file, tips_android_studio_dir,
             tips_github_pages_cn_dir],
        ]
        iox.choose_action(action_list)

    def process_tips_manifest_file(self, file_path, result_file=None):
        """
        处理清单文件，整理tips的名称方便翻译
        :param file_path:
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file_path, '_name', 'properties')
        ordered_file_list = self.get_tips_order_files(file_path)

        result = []
        for file in ordered_file_list:
            name = file.split('.')[0]
            word = self.camel_word_to_words(name)
            result.append('%s=%s\n' % (name, word))
        filex.write_lines(result_file, result)

    @staticmethod
    def camel_word_to_words(word):
        """
        驼峰转为多个单词，如果是大写缩写则不变
        :param word: 
        :return: 
        """
        result = re.sub('[A-Z][a-z]+', lambda m: m.group().lower() + ' ', word).rstrip()
        # 少数情况，要再处理一次
        result = result.replace('Ifor', 'I for').replace('movefile', 'move file')
        if word != result:
            print('【%s】转为【%s】' % (word, result))
        else:
            print('%s无变化' % word)
        return result

    @staticmethod
    def process_all_github_pages():
        """处理为github page"""
        for param in Tips.github_pages_action_list:
            Tips.process_tips_translation_result(param[0], param[1], Tips.RESULT_TYPE_GITHUB_PAGES,
                                                 param[2], param[3], param[4])

    @staticmethod
    def process_tips_translation_result(tips_names_file, tips_cn_dir, result_type=RESULT_TYPE_ANDROID_STUDIO,
                                        result_dir=None, result_file_type=0, language='cn'):
        """
        处理OmegaT翻译的tips的结果
        :param tips_cn_dir:
        :param tips_names_file:
        :param result_type: 0为AndroidStudio,1为GitHub Page
        :param result_dir:
        :param result_file_type: 结果文件类型，0为数字，1为数字加名字
        :param language: 语言
        :return:
        """
        if result_dir is None:
            if result_type == Tips.RESULT_TYPE_GITHUB_PAGES:
                result_dir = tips_cn_dir + '_github_page'
            else:
                result_dir = tips_cn_dir + "_android_studio"
        if language == 'en':
            Tips.KEYMAP_DICT = Tips.KEYMAP_EN_DICT
        else:
            Tips.KEYMAP_DICT = Tips.KEYMAP_CN_DICT

        print('处理' + tips_cn_dir)

        file_dict = Tips.get_file_dict_in_dir(tips_cn_dir)
        if file_dict is None:
            return

        lines = filex.read_lines(tips_names_file, ignore_line_separator=True)
        if lines is None:
            return

        length = len(lines)
        for i in range(length):
            line = lines[i]
            en_name, cn_name = line.split('=')
            if en_name in file_dict.keys():
                file_name = file_dict[en_name]
                if language == 'cn':
                    add_cn_title = '(%s)' % cn_name
                else:
                    add_cn_title = ''
                header = '<h1>[%d/%d] %s%s</h1>\n' % (i + 1, length, en_name, add_cn_title)
                if result_type == Tips.RESULT_TYPE_ANDROID_STUDIO:
                    footer = None
                    result_name = file_name.replace(tips_cn_dir, result_dir)
                else:
                    # 前一页
                    pre_page = ''
                    if i > 0:
                        pre_name = lines[i - 1].split('=')[0]
                        if result_file_type == 1:
                            pre_file = '%03d-%s.html' % (i, pre_name)
                        else:
                            pre_file = '%03d.html' % i
                        pre_page = '<a href=\'%s\'>&lt;&lt;%s</a>' % (pre_file, pre_name)

                    # 后一页
                    next_page = ''
                    if i < length - 1:
                        next_name = lines[i + 1].split('=')[0]
                        if result_file_type == 1:
                            next_file = '%03d-%s.html' % (i + 2, next_name)
                        else:
                            next_file = '%03d.html' % (i + 2)
                        next_page = '<a href=\'%s\'>&gt;&gt;%s</a>' % (next_file, next_name)

                    # 当前文件名和结果名
                    dir_name, base_name = os.path.split(file_name)
                    name, ext = os.path.splitext(base_name)
                    if result_file_type == 1:
                        current_file = '%03d-%s.html' % (i + 1, name)
                    else:
                        current_file = '%03d%s' % (i + 1, ext)
                    result_name = '%s\\%s' % (result_dir, current_file)

                    # 主页
                    home_page = '<a href=\'%s\'>homepage</a>' % '../index.html'
                    # 切换页面
                    if language == 'cn':
                        to_another_page = '<a href=\'../%s/%s\'>English</a>' % ('en', current_file)
                    else:
                        to_another_page = '<a href=\'../%s/%s\'>中文</a>' % ('cn', current_file)
                    add_homepage = '<p>%s&nbsp;|&nbsp;%s</p>\n' % (home_page, to_another_page)

                    header = add_homepage + header
                    footer = '<p>%s&nbsp;&nbsp;%s</p>\n<p>&nbsp;</p>' % (pre_page, next_page)

                Tips.process_tips_translation_file(file_name, result_name, result_type, header, footer, language)

    @staticmethod
    def process_tips_translation_file(file_path, result_file, result_type, add_header=None, add_footer=None,
                                      language='cn'):
        """
        处理翻译的tip文件，将
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        删除，这是OmegaT自动添加的，添加后AndroidStudio反而不能正常加载了。
        然后&符号需要转义回去。
        :param file_path:
        :param result_file:
        :param result_type: AndroidStudio中需要删除meta
        :param add_header: 添加header
        :param add_footer: 添加footer
        :param language: 语言
        :return:
        """
        lines = filex.read_lines(file_path)
        if lines is None:
            return
        meta = r'<meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        result = []
        add_meta = False
        for line in lines:
            if result_type == Tips.RESULT_TYPE_GITHUB_PAGES or meta not in line:
                if not add_meta and language == 'en':
                    if '<link rel=' in line:
                        # 添加meta
                        result.append(meta)
                        add_meta = True
                # 替换并添加
                line = Tips.parse_line(line, result_type)
                result.append(line)
                # 添加header
                if add_header is not None and line.lstrip().startswith('<body'):
                    result.append(add_header)
                    if add_footer is not None:
                        # 还是放上面好了
                        result.append(add_footer)
        filex.write_lines(result_file, result, print_msg=True)

    @staticmethod
    def parse_line(line, result_type):
        """解析每一行中的参数"""
        result = line
        result = result.replace('&amp;', '&')
        if result_type == Tips.RESULT_TYPE_GITHUB_PAGES:
            result = result.replace('"css/tips.css"', '"../css/tips.css"')
            result = result.replace('"images/', '"../images/')
            # 解析快捷键
            result = re.sub(r'&shortcut:(\w+);', Tips.replace_shortcut, result)
            # 解析变量
            result = re.sub(r'&(?!lt|gt|nbsp|quot)(\w+);', Tips.replace_variable, result)
        return result

    @staticmethod
    def replace_shortcut(match):
        shortcut_id = match.group(1)
        if shortcut_id in Tips.KEYMAP_DICT.keys():
            result = Tips.KEYMAP_DICT[shortcut_id]
            # print('解析%s为%s' % (shortcut_id, result))
        else:
            result = shortcut_id
            print('没有找到快捷键' + shortcut_id)
        return result

    @staticmethod
    def replace_variable(match):
        variable = match.group(1)
        if variable in Tips.VARIABLE_DICT.keys():
            result = Tips.VARIABLE_DICT[variable]
            # print('解析%s为%s' % (variable, result))
        else:
            result = variable
            print('没有找到变量' + variable)
        return result

    @staticmethod
    def order_tips_file(tips_names_file, processed_dir, result_dir):
        """
        排序tips的翻译文件
        :param tips_names_file:
        :param processed_dir:
        :param result_dir:
        :return:
        """

        file_dict = Tips.get_file_dict_in_dir(processed_dir)
        if file_dict is None:
            return

        lines = filex.read_lines(tips_names_file, ignore_line_separator=True)
        if lines is None:
            return

        length = len(lines)
        for i in range(length):
            line = lines[i]
            en_name, cn_name = line.split('=')
            if en_name in file_dict.keys():
                old_name = file_dict[en_name]
                dir_name, file_name = os.path.split(old_name)
                new_name = '%s\\%03d-%s' % (result_dir, i + 1, file_name)
                print('复制%s为%s' % (old_name, new_name))
                filex.check_and_create_dir(new_name)
                shutil.copy(old_name, new_name)
            else:
                print('没有文件' + en_name)

    @staticmethod
    def get_file_dict_in_dir(dir_path):
        """
        获取目录中的文件，组成以文件名（不带后缀的）为key的字典
        :param dir_path:
        :return:
        """
        file_dict = dict()
        for parent, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                name, ext = os.path.splitext(file)
                if ext == '.html' and not parent.endswith('excluded'):
                    file_dict[name] = parent + '\\' + file
        return file_dict

    @staticmethod
    def get_tips_order_files(order_file):
        """
        获取tips的顺序
        :param order_file: 读取的文件，位于lib/resources.jar，/META-INF/IdeTipsAndTricks.xml
        :return:
        """
        tree = Et.parse(order_file)
        root = tree.getroot()
        order_files = []
        for tu in root.iter('tipAndTrick'):
            order_files.append(tu.attrib['file'])
        return order_files


if __name__ == '__main__':
    Tips().main()
