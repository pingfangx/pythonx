import re
from xml.etree import ElementTree as Et

from xx import filex


class DeleteAction:
    """删除操作"""

    FILE_TYPE_FILE = 0
    "文件"

    FILE_TYPE_OMEGAT = 1
    "OmegaT的记忆文件"

    DELETE_TYPE_ELLIPSIS = 0
    "删除省略号"

    DELETE_TYPE_SPACE = 1
    "删除等号前后的空格"

    DELETE_TYPE_UNDERLINE_SHORTCUT = 2
    "删除下划线样式的快捷方式，**注意这个会删除所有下划线，小心使用**"

    DELETE_TYPE_AND_SHORTCUT = 3
    "删除&样式的快捷方式"

    action_list = [
        [
            0, '省略号', '_delete_ellipsis', [r'(\s?([.。…\\:])+)$', '', 1, '%s']
        ],
        [
            1, '等号前后的空格', '_delete_space', ['\s*(=)\s*', r'\1']
        ],
        [
            2, '_样式的快捷方式', '_delete_underline_shortcut', [r'_(\w)', r'\1', 1, '(_%s)']
        ],
        [
            3, '&样式的快捷方式', '_delete_and_short_cut', [r'(?<!\\)&(\w)', r'\1', 1, '(&%s)']
        ]
    ]
    """
    第个操作包括[序号，名字，结果文件名添加，替换列表...]
    替换列表可能是多个
    每个替换列表包所[查找正则，替换为，反向恢复时要添加的内容的group的序号（，可选），添加时的字符串模板]
    """

    def __init__(self, name, delete_type, file_type, default_result_file_suffix, replace_list):
        """
        
        :param name: 
        :param delete_type: 删除类型，0为省略号，1为快捷方式,2为省略号前后的空格
        :param file_type: 文件类型，0为文件，1为omega，omega的文件要小心处理，只有首次导入时应该处理，后面可能已翻译好了。
        :param default_result_file_suffix: 
        :param replace_list: 
        """
        self.name = name
        self.delete_type = delete_type
        self.file_type = file_type
        self.default_result_file_suffix = default_result_file_suffix
        self.replace_list = replace_list

    @staticmethod
    def delete_ellipsis(file, result_file):
        DeleteAction.delete_symbol(DeleteAction.DELETE_TYPE_ELLIPSIS, file, DeleteAction.FILE_TYPE_FILE, result_file)

    @staticmethod
    def delete_space(file, result_file):
        DeleteAction.delete_symbol(DeleteAction.DELETE_TYPE_SPACE, file, DeleteAction.FILE_TYPE_FILE, result_file)

    @staticmethod
    def delete_underline_shortcut(file, result_file):
        DeleteAction.delete_symbol(DeleteAction.DELETE_TYPE_UNDERLINE_SHORTCUT, file, DeleteAction.FILE_TYPE_FILE,
                                   result_file)

    @staticmethod
    def delete_and_shortcut(file, result_file):
        DeleteAction.delete_symbol(DeleteAction.DELETE_TYPE_AND_SHORTCUT, file, DeleteAction.FILE_TYPE_FILE,
                                   result_file)

    @staticmethod
    def delete_symbol(delete_type, file, file_type=0, result_file=None):
        delete_action = DeleteAction.action_list[delete_type]
        if result_file is None:
            result_file = filex.get_result_file_name(file, delete_action[2])
        if file_type == DeleteAction.FILE_TYPE_OMEGAT:
            DeleteAction.delete_symbol_of_omegat(file, result_file, delete_action[3:])
        else:
            DeleteAction.delete_symbol_of_file(file, result_file, delete_action[3:])

    @staticmethod
    def delete_symbol_of_file(file, result_file, replace_list):
        lines = filex.read_lines(file)
        if lines is None:
            return
        result = []
        for line in lines:
            line = line.replace('\n', '')
            if line is None:
                continue
            old_line = line
            for replace_pattern in replace_list:
                line = re.sub(replace_pattern[0], replace_pattern[1], line)
                if old_line != line:
                    print('处理【%s】为【%s】' % (old_line, line))
            result.append(line + '\n')

        filex.write_lines(result_file, result)

    @staticmethod
    def delete_symbol_of_omegat(file, result_file, replace_list):
        tree = Et.parse(file)
        tmx = tree.getroot()
        body = tmx.find('body')
        for seg in body.iter('seg'):
            line = seg.text
            if line is None:
                continue
            old_line = line
            for replace_pattern in replace_list:
                line = re.sub(replace_pattern[0], replace_pattern[1], line)
                if old_line != line:
                    print('处理【%s】为【%s】' % (old_line, line))
            seg.text = line
        tree.write(result_file, encoding='utf-8')
        print('输出为' + result_file)

    @staticmethod
    def delete_all_symbol_of_string(text, print_msg=False):
        """删除文字中的所有标记"""
        result = text
        for action in DeleteAction.action_list:
            replace_list = action[3:]
            for replace_pattern in replace_list:
                pre_result = result
                result = re.sub(replace_pattern[0], replace_pattern[1], result)
                if print_msg:
                    if pre_result != result:
                        print('\n缩简【%s】为【%s】' % (pre_result, result))
        return result

    @staticmethod
    def add_extra_info_of_string(en, cn, print_msg=False):
        """为翻译结果添加快捷键等信息"""
        result = cn
        for action in DeleteAction.action_list:
            replace_list = action[3:]
            for replace_pattern in replace_list:
                if len(replace_pattern) >= 4:
                    # 有可以添加的值
                    group_index = replace_pattern[2]
                    append = replace_pattern[3]
                    match = re.search(replace_pattern[0], en)
                    if match is not None:
                        # 匹配
                        pre_result = result
                        append_content = match.group(group_index)
                        if append_content == '.':
                            # .换为句号
                            append_content = '。'
                        append_content = append % append_content
                        if not result.endswith(append_content):
                            # 已经以。等结尾，不添加
                            result += append_content
                        if print_msg:
                            print('匹配%s,处理\n【%s】为\n【%s】' % (replace_pattern[0], pre_result, result))

        if print_msg:
            if result == cn:
                print('%s没有发生变化' % en)
        return result
