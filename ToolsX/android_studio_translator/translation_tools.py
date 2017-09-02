from xx import filex
import re


def delete_shortcut(file, result_file=None):
    """
    删除文件中的快捷方式
    :param file:
    :param result_file:
    :return:
    """
    if result_file is None:
        result_file = filex.get_result_file_name(file, '_delete_shortcut')
    lines = filex.read_lines(file)
    if lines is None:
        return
    # (.*懒惰)(空白?点一次或多次)
    p = re.compile(r'(.*?)(\s?\(_\w\))')
    result = []
    for line in lines:
        line = line.replace('\n', '')
        if line is None:
            continue
        if '_' in line:
            if re.match(p, line) is not None:
                replace_result = re.sub(p, r'\1', line)
                print('删除【%s】为【%s】' % (line, replace_result))
            else:
                replace_result = line.replace('_', '')
                print('替换【%s】为【%s】' % (line, replace_result))
            line = replace_result
        result.append(line + '\n')

    filex.write_lines(result_file, result)
    print('输出为' + result_file)


def delete_ellipsis(file, result_file=None):
    """
    删除每一行结尾的“.”，包括一个（句号）或多个（如省略号）
    :param file:
    :param result_file:
    :return:
    """
    if result_file is None:
        result_file = filex.get_result_file_name(file, '_delete_ellipsis')
    lines = filex.read_lines(file)
    if lines is None:
        return
    # (.*懒惰)(空白?点一次或多次)
    p = re.compile(r'(.*?)(\s?\.+)$')
    result = []
    for line in lines:
        line = line.replace('\n', '')
        if line is None:
            continue
        if '.' in line:
            if re.match(p, line) is not None:
                replace_result = re.sub(p, r'\1', line)
                print('删除【%s】为【%s】' % (line, replace_result))
                line = replace_result
            else:
                print('未处理【%s】' % line)
        result.append(line + '\n')

    filex.write_lines(result_file, result)
    print('输出为' + result_file)


def get_dict_from_file(file_path, separator='=', delete_value_ellipsis=True, delete_value_underline=True):
    """
    从文件中读取字典，
    :param file_path:文件路径
    :param separator:分隔符
    :return: 如果有错返回None
    :param delete_value_ellipsis:删除省略号
    :param delete_value_underline: 删除快捷方式
    """
    result = filex.get_dict_from_file(file_path, separator)
    if result is None:
        return None

    if delete_value_ellipsis or delete_value_underline:
        # (空白?点一次或多次)
        p_ellipsis = re.compile(r'(\s?\.+)$')
        for key, value in result.items():
            if delete_value_ellipsis:
                value = re.sub(p_ellipsis, '', value)
            if delete_value_underline:
                value = value.replace('_', '')
            result[key] = value
    return result
