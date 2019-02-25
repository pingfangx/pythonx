import re

from tool.android.android_studio_translator import ActionsBundle
from tool.android.android_studio_translator.tools import Tools
from xx import encodex
from xx import filex
from xx import iox


class KeymapList:
    """
    AndroidStudio设置中的所有keymap
    [AndroidStudio翻译(2)-keymap中的所有操作的中文翻译](http://blog.pingfangx.com/2354.html)
    """

    def main(self):
        keymap_file = r'data/keymap.txt'
        """所有keymap的文件"""

        en_add_file = '../actions_bundle/' + ActionsBundle.en_add_file

        keymap_comment_file = r'data/keymap_comment.properties'
        """注释文件，是旧版本时添加的，读取到新版本中"""

        keymap_delete_ellipsis_file = r'data/keymap_delete_ellipsis.txt'
        """删除省略号的文件，选删除省略号，再添加注释"""

        keymap_list_result_file = 'data/keymap_list.md'
        """结果文件"""

        action_list = [
            ['退出', exit],
            ['读取描述字典', self.get_action_desc_dict, en_add_file, True],
            ['读取注释字典', self.get_comment_dict, keymap_comment_file, True],
            ['删除末尾的省略号', Tools.delete_ellipsis, keymap_file],
            ['增加描述、注释并导出为要翻译的文件', self.handle_keymap_file, en_add_file, keymap_delete_ellipsis_file,
             keymap_comment_file],
            ['处理翻译完的keymap文件', self.process_translated_keymap_file,
             r'D:\workspace\TranslatorX\AndroidStudio\source\keymap_delete_ellipsis_add_desc_and_comment.properties',
             r'D:\workspace\TranslatorX\AndroidStudio\target\keymap_delete_ellipsis_add_desc_and_comment_zh_CN'
             r'.properties', keymap_list_result_file],
        ]
        iox.choose_action(action_list)

    def action1(self, param):
        pass

    @staticmethod
    def handle_keymap_file(en_file, cn_file, comment_file, result_file=None):
        """
        将一行一行的keymap重新处理
        导出为.properties，这样OmegaT处理时会换照配置文件去处理
        我们以[#]或[desc]加空格为开头，会被过滤器正确解析
        :param en_file:
        :param cn_file:
        :param comment_file:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_add_desc_and_comment', 'properties')

        lines = filex.read_lines(cn_file)
        if lines is None:
            return

        desc_dict = KeymapList.get_action_desc_dict(en_file)
        comment_dict = KeymapList.get_comment_dict(comment_file)

        count = 0
        desc_count = 0
        result = []
        for line in lines:
            line = line.replace('\n', '')
            if line.startswith('#'):
                old_line = line
                # 因为有加了#，所以处理下
                line = line.lstrip('# ')
                # 相差的长度是trip掉的，注意在替换了\n之后
                prefix = old_line[0:len(old_line) - len(line)].rstrip()
            else:
                prefix = '#' * 5
            append = ''
            count += 1
            if line in desc_dict.keys():
                desc = desc_dict[line]
                desc_count += 1
                print('%d/%d,line=%s,desc=%s' % (count, desc_count, line, desc))
                # 有描述，添加
                append += '\n\n%s %s' % ('[desc]', desc)
            if line in comment_dict.keys():
                comment = comment_dict[line]
                print('%s的描述为%s' % (line, comment))
                append += '\n\n%s' % comment
            line = '\n\n[%s] %s%s' % (prefix, line, append)
            result.append(line)
        filex.write_lines(result_file, result)

    @staticmethod
    def get_action_desc_dict(en_file, print_msg=False):
        """
        读取操作对应的描述
        :param en_file:
        :param print_msg:
        :return:
        """

        en_dict = Tools.get_dict_from_file(en_file)
        desc_dict = dict()
        # 重复的处理起来麻烦，索性删除了
        duplicate_value = list()
        # 反转
        for key, value in en_dict.items():
            if key.endswith('.text'):
                desc_key = key[:-len('.text')] + '.description'
                if desc_key in en_dict.keys():
                    desc = en_dict[desc_key]
                    if value in desc_dict.keys():
                        pre_desc = desc_dict[value]
                        if desc == pre_desc:
                            print('%s重复【%s】' + value, desc)
                        else:
                            duplicate_value.append(value)
                            desc = '%s【或】%s' % (pre_desc, desc)
                            print('%s有不同的描述【%s】【%s】' % (value, desc, pre_desc))
                    desc_dict[value] = desc
        for value in duplicate_value:
            if value in desc_dict.keys():
                desc_dict.pop(value)
                if print_msg:
                    print('删除' + value)
        if print_msg:
            print(desc_dict)
        return desc_dict

    @staticmethod
    def get_comment_dict(file_path, print_msg=False):
        """
        读取注释字典，用于新的keymap读取注释
        :param file_path:
        :param print_msg:
        :return:
        """
        lines = filex.read_lines(file_path, ignore_line_separator=True)
        if lines is None:
            return
        comment_dict = dict()
        p_title = re.compile(r'\[(#+)\]\s?')
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('#[x'):
                # 是注释
                pre_index = i - 1
                action = ''
                while action == '' and pre_index >= 0:
                    pre_line = lines[pre_index]
                    if pre_line.startswith('[#'):
                        action = re.sub(p_title, '', pre_line)
                        comment = line
                        if action in comment_dict.keys():
                            if print_msg:
                                print('%s注释重复' % action)
                            comment = comment_dict[action] + '\n' + comment
                        comment_dict[action] = comment
                        if print_msg:
                            print('%s的注释为%s' % (action, comment))
                    pre_index -= 1
        return comment_dict

    @staticmethod
    def process_translated_keymap_file(en_file, cn_file, result_file=None):
        """
        处理翻译完的文件
        :param en_file:
        :param cn_file:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_final')
        en_lines = filex.read_lines(en_file)
        cn_lines = filex.read_lines(cn_file)
        if cn_lines is None:
            return

        result = []
        p_title = re.compile(r'^\[(#+)\]\s?(.*)')
        p_title2 = re.compile(r'(\n*)(#+\s)(.*)')
        p_desc = re.compile(r'^\[desc\]\s?(.*)')
        p_comment = re.compile(r'^#\[(x+)\](.*)')
        for i in range(len(cn_lines)):
            line = cn_lines[i].replace('\n', '')
            if line.startswith('#'):
                # 以#开头不翻译，取原文
                line = en_lines[i].replace('\n', '')
                match = re.match(p_comment, line)
                if match is not None:
                    # 注释
                    start_number = match.group(1)
                    if len(start_number) == 1:
                        # 1颗星标记基本注释
                        replace_result = '  \n译注：%s' % (match.group(2))
                    else:
                        # 2星以上为加重注释
                        # 向上寻找标题并加重
                        last_index = -1
                        while result[last_index] == '' or re.match(p_title2, result[last_index]) is None:
                            last_index -= 1
                        last_line = result[last_index]
                        if '★' not in last_line:
                            start_replace = '★' * (len(start_number) - 1)
                            last_line = re.sub(p_title2, r'\1\2*%s\3%s*' % (start_replace, start_replace),
                                               last_line)
                            print('替换标题【%s】为【%s】' % (result[last_index], last_line))
                            result[last_index] = last_line
                        replace_result = '  \n译注：%s' % (match.group(2))
                    # print('替换【%s】为【%s】' % (line, replace_result))
                    line = '%s' % replace_result
            else:
                # 不以#开头
                line = encodex.unicode_str_to_chinese(line)
                en_line = en_lines[i].replace('\n', '')
                match = re.match(p_title, line)
                if match is not None:
                    # 是标题
                    en_match = re.match(p_title, en_line)
                    if len(en_match.group(1)) == 5:
                        replace_result = '\n\n%s（%s）' % (en_match.group(2), match.group(2))
                    else:
                        replace_result = '\n\n%s %s（%s）' % (en_match.group(1), en_match.group(2), match.group(2))
                    # print('\n替换【%s】为【%s】' % (line, replace_result))
                    line = '%s' % replace_result
                else:
                    desc_cn_match = re.match(p_desc, line)
                    if desc_cn_match is not None:
                        # 是描述
                        desc_en_match = re.match(p_desc, en_line)
                        replace_result = '  \n%s  \n描述：%s' % (desc_en_match.group(1), desc_cn_match.group(1))
                        # print('\n描述替换【%s】为【%s】' % (line, replace_result))
                        line = '%s' % replace_result

            result.append(line)
        filex.write_lines(result_file, result)


if __name__ == '__main__':
    KeymapList().main()
