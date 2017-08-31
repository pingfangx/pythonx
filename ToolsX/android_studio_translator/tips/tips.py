import os
from xml.etree import ElementTree as Et

from xx import filex
from xx import iox
import shutil


class Tips:
    def main(self):
        # 翻译结果
        tips_cn_dir = r'E:\workspace\TranslatorX\AndroidStudio\target\tips'
        # 翻译结果处理后的目录
        tips_processed_dir = tips_cn_dir + '_processed'

        # 排序文件
        tips_order_file = r'IdeTipsAndTricks.xml'
        # 排序后的目灵
        tips_order_dir = tips_cn_dir + '_order'

        # 文件名翻译结果
        tips_names_cn_file = r'IdeTipsAndTricks_name_zh_CN_cn_result.properties'
        action_list = [
            ['退出', exit],
            ['处理顺序文件方便翻译', self.process_read_order_file, tips_order_file],
            ['处理tips翻译结果为AndroidStudio用', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir, 0,
             tips_processed_dir],
            ['处理tips翻译结果为GitHub Page用', self.process_tips_translation_result, tips_names_cn_file, tips_cn_dir, 1,
             tips_order_dir],
            ['将处理结果排序', self.order_tips_file, tips_names_cn_file, tips_processed_dir, tips_order_dir]
        ]
        iox.choose_action(action_list)

    def process_read_order_file(self, order_file, result_file=None):
        """
        处理顺序文件翻便翻译
        :param order_file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(order_file, '_name', 'properties')
        ordered_file_list = self.get_tips_order_files(order_file)

        result = []
        for file in ordered_file_list:
            name = file.split('.')[0]
            word = self.camel_word_to_words(name)
            result.append('%s=%s\n' % (name, word))
        filex.write_lines(result_file, result)

    @staticmethod
    def camel_word_to_words(word):
        """
        驼峰转为多个单词
        :param word: 
        :return: 
        """
        result = ""
        for a in word:
            # 字母比较，无需判断
            # noinspection PyTypeChecker
            if 'A' <= a <= 'Z':
                if result != '':
                    result += ' ' + a.lower()
                else:
                    result += a.lower()
            else:
                result += a
        return result

    def process_tips_translation_result(self, tips_names_file, tips_cn_dir, result_type=0, result_dir=None):
        """
        处理OmegaT翻译的tips的结果
        :param tips_cn_dir:
        :param tips_names_file: 
        :param result_type: 
        :param result_dir:
        :return:
        """
        if result_dir is None:
            result_dir = tips_cn_dir + "_result"

        print('处理' + tips_cn_dir)

        file_dict = self.get_file_dict_in_dir(tips_cn_dir)
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
                header = '<h1>[%d/%d] %s(%s)</h1>\n' % (i + 1, length, en_name, cn_name)
                if result_type == 0:
                    footer = None
                    result_name = file_name.replace(tips_cn_dir, result_dir)
                else:
                    # 前一页
                    pre_page = ''
                    if i > 0:
                        pre_name = lines[i - 1].split('=')[0]
                        pre_file = '%03d-%s.html' % (i, pre_name)
                        pre_page = '<a href=\'%s\'>&lt;&lt;%s</a>' % (pre_file, pre_name)

                    # 后一页
                    next_page = ''
                    if i < length - 1:
                        next_name = lines[i + 1].split('=')[0]
                        next_file = '%03d-%s.html' % (i + 2, next_name)
                        next_page = '<a href=\'%s\'>&gt;&gt;%s</a>' % (next_file, next_name)

                    footer = '<p>&nbsp;</p><p>%s&nbsp;&nbsp;%s</p>\n' % (pre_page, next_page)
                    dir_name, base_name = os.path.split(file_name)
                    result_name = '%s\\%03d-%s' % (result_dir, i + 1, base_name)
                self.process_tips_translation_file(file_name, result_name, header, footer)

    @staticmethod
    def process_tips_translation_file(file_path, result_file, add_header=None, add_footer=None):
        """
        处理翻译的tip文件，将
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        删除，这是OmegaT自动添加的，添加后AndroidStudio反而不能正常加载了。
        然后&符号需要转义回去。
        :param file_path:
        :param result_file:
        :param add_header: 添加header
        :param add_footer: 添加footer
        :return:
        """
        lines = filex.read_lines(file_path)
        if lines is None:
            return
        meta = r'<meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        result = []
        for line in lines:
            if meta not in line:
                # 添加footer
                if add_footer is not None and line.lstrip().startswith('</body>'):
                    result.append(add_footer)
                # 替换并添加
                line = line.replace('&amp;', '&')
                result.append(line)
                # 添加header
                if add_header is not None and line.lstrip().startswith('<body'):
                    result.append(add_header)
        filex.write_lines(result_file, result)

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
                name = os.path.splitext(file)[0]
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
