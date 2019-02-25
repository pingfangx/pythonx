import os
import re
import shutil
from xml.etree import ElementTree as Et

from tool.android.android_studio_translator import Version
from tool.android.android_studio_translator.keymap_default.keymap_default import KeymapDefault
from tool.android.android_studio_translator.tools import Tools
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

    KEYMAP_CN_DICT = KeymapDefault.get_keymap_dict_from_file('../keymap_default/data/$default.xml')
    KEYMAP_CN_DICT.update(KeymapDefault.get_keymap_dict_from_file('../tips/data/keymap_add.xml'))
    KEYMAP_EN_DICT = KeymapDefault.get_keymap_dict_from_file('../keymap_default/data/$default.xml', False)
    KEYMAP_EN_DICT.update(KeymapDefault.get_keymap_dict_from_file('../tips/data/keymap_add.xml', False))

    KEYMAP_DICT = KEYMAP_CN_DICT

    github_pages_action_list = list()

    def main(self):
        tips_en_dir = Version.source_version_lib_resource_en + '/tips'
        # 翻译结果目录
        tips_cn_dir = Version.target_version_lib + '/resources_en/tips'
        # 处理为AndroidStudio的目录
        tips_android_studio_dir = tips_cn_dir + r'_android_studio'
        # 处理为github page的目录
        tips_github_pages_en_dir = r'D:\workspace\github.pingfangx.io\android_studio\tips' + r'\en'
        tips_github_pages_cn_dir = r'D:\workspace\github.pingfangx.io\android_studio\tips' + r'\cn'

        # 清单文件
        tips_manifest_file = Version.original_version_lib + '/resources/META-INF/IdeTipsAndTricks.xml'
        tips_name_en_file = Version.source_version_lib + '/resources/META-INF/IdeTipsAndTricks_en.properties'
        tips_manifest_translation_file = Version.target_version_lib + '/resources/META-INF/IdeTipsAndTricks_en_zh_CN' \
                                                                      '.properties '

        # 文件名翻译结果
        tips_names_cn_file = Version.target_version_lib + '/resources/META-INF/IdeTipsAndTricks_en_zh_CN_cn_result' \
                                                          '.properties '

        Tips.github_pages_action_list = [
            [tips_names_cn_file, tips_en_dir, tips_github_pages_en_dir, 0, 'en'],
            [tips_names_cn_file, tips_en_dir, tips_github_pages_en_dir, 1, 'en'],
            [tips_names_cn_file, tips_cn_dir, tips_github_pages_cn_dir, 0, 'cn'],
            [tips_names_cn_file, tips_cn_dir, tips_github_pages_cn_dir, 1, 'cn'],
        ]
        action_list = [
            ['退出', exit],
            ['处理清单文件，整理tips的名称方便翻译', self.process_tips_manifest_file, tips_manifest_file, tips_name_en_file],
            ['检查并补全缺少的tips名', self.check_and_append_tips_name, tips_en_dir, tips_name_en_file, tips_name_en_file],
            ['将翻译结果的unicode转为中文', Tools.change_unicode_to_chinese, tips_manifest_translation_file],
            ['处理tips翻译结果为AndroidStudio用', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir,
             Tips.RESULT_TYPE_ANDROID_STUDIO, tips_android_studio_dir],
            ['处理tips翻译结果为AndroidStudio用（重命名原始目录）', self.process_tips_to_android_studio, tips_names_cn_file,
             tips_cn_dir],
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
            result_file = filex.get_result_file_name(file_path, '_en', 'properties')
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
        result = result.replace('Ifor', 'I for').replace('movefile', 'move file').replace('html 5outline',
                                                                                          'html5 outline')
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
    def process_tips_to_android_studio(tips_names_file, tips_cn_dir):
        """
        处理为AndroidStudio的结果
        :param tips_names_file: 
        :param tips_cn_dir: 
        :return: 
        """
        back_dir = tips_cn_dir + '_back'
        if os.path.exists(back_dir):
            print('删除文件夹%s' % back_dir)
            shutil.rmtree(back_dir)
        print('重命名')
        os.rename(tips_cn_dir, back_dir)
        Tips.process_tips_translation_result(tips_names_file, back_dir, Tips.RESULT_TYPE_ANDROID_STUDIO, tips_cn_dir)

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

        file_dict = Tips.get_file_dict_in_dir(tips_cn_dir, ignore_excluded=True)
        if file_dict is None:
            return

        all_lines = filex.read_lines(tips_names_file, ignore_line_separator=True)
        if all_lines is None:
            return

        # 删除空行
        lines = []
        append_line = -1
        for line in all_lines:
            if '=' in line:
                lines.append(line)
            else:
                if 'append' in line:
                    # 有几个就从第几个开始，如果有1个，则index从1开始是添加的
                    append_line = len(lines)

        length = len(lines)
        print('共%d行，添加行是%d' % (length, append_line))
        all_files = filex.list_file(tips_cn_dir)
        print('共%d文件' % len(all_files))
        for i in range(length):
            line = lines[i]
            en_name, cn_name = line.split('=')
            file_path = r'%s\%s.html' % (tips_cn_dir, en_name)
            if i >= append_line or not os.path.exists(file_path):
                # 如果是添加的或不存在，取exclude的
                excluded_file_path = r'%s\excluded\%s.html' % (tips_cn_dir, en_name)
                if os.path.exists(excluded_file_path):
                    # 如果存在则赋值，否则可能顺序在后，其实文件还是在前
                    file_path = excluded_file_path
            if not os.path.exists(file_path):
                print('文件不存在%s' % en_name)
                continue
            # 已经有了，移除
            if file_path in all_files:
                all_files.remove(file_path)
            else:
                # 该错误的原因是在 IdeTipsAndTricks 中有 2 个相同的名字
                print('文件不存于列表中%s' % file_path)
            if language == 'cn':
                add_cn_title = '(%s)' % cn_name
            else:
                add_cn_title = ''
            header = '<h1>%s%s</h1>\n' % (en_name, add_cn_title)
            if result_type == Tips.RESULT_TYPE_ANDROID_STUDIO:
                author_url = '<a href=\'%s\'>[%s]</a>' % (
                    'https://www.pingfangx.com/xx/translation/feedback?from=tips',
                    '汉化反馈')
                header = '<h1>%s%s %s</h1>\n' % (en_name, add_cn_title, author_url)
                footer = None
                result_name = file_path.replace(tips_cn_dir, result_dir)
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
                dir_name, base_name = os.path.split(file_path)
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

            Tips.process_tips_translation_file(file_path, result_name, result_type, header, footer, language)
        print('剩余文件%d个' % len(all_files))
        if len(all_files) > 0:
            print('**请补全文件**')
            # 如果确认不需要补全（如在 exclude 中包含文件），可以不退出
            # exit()

    @staticmethod
    def check_and_append_tips_name(file_path, tips_name_file, result_file=None):
        """
        根据检查tips的文件是否全
        该方法用于 IdeTipsAndTricks 没有指定所有的文件，但还是需要翻译文件名的，所以补全
        """
        if result_file is None:
            result_file = filex.get_result_file_name(tips_name_file, '_append')
        file_list = filex.list_file(file_path)
        print('共%d个文件' % len(file_list))
        lines = filex.read_lines(tips_name_file)
        tips_name = []
        for line in lines:
            if '=' in line:
                name = line.split('=')[0]
                tips_name.append(name)
                # 名字只加一层，exclude里面的不处理
                file_name = '%s\\%s.html' % (file_path, name)
                if file_name in file_list:
                    file_list.remove(file_name)
                else:
                    print('文件不存在%s' % file_name)
        print('共有%d个tip名' % len(tips_name))
        print('还缺%d个文件' % len(file_list))
        # 写入结果
        lines.append('\n# append\n')
        for file_name in file_list:
            name = os.path.splitext(os.path.split(file_name)[1])[0]
            word = Tips.camel_word_to_words(name)
            lines.append('%s=%s\n' % (name, word))
        filex.write_lines(result_file, lines)

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

        if add_header and add_header in lines:
            # 不重复添加
            add_header = None

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
        filex.write_lines(result_file, result, print_msg=False)

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
    def get_file_dict_in_dir(dir_path, ignore_excluded=False):
        """
        获取目录中的文件，组成以文件名（不带后缀的）为key的字典
        :param dir_path:
        :param ignore_excluded: 是否忽略exclude的
        :return:
        """
        file_dict = dict()
        for parent, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                name, ext = os.path.splitext(file)
                if ext == '.html':
                    if not (ignore_excluded and parent.endswith('excluded')):
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
