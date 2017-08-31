import os.path


def read_lines(file_path, encoding='utf-8', ignore_line_separator=False):
    """
    读取所有行
    :param file_path: 文件路径
    :param encoding: 编码
    :param ignore_line_separator: 是否忽略换行符
    :return:
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, encoding=encoding) as f:
        if ignore_line_separator:
            result = [line.replace('\n', '') for line in f.readlines()]
        else:
            result = f.readlines()
    return result


def write_lines(file_path, lines, add_line_separator=False, print_msg=True):
    """
    写入翻译结果
    :param file_path: 要写入的文件
    :param lines: 结果数组
    :param add_line_separator: 是否添加换行符
    :param print_msg: 是否显示
    :return: 
    """
    if add_line_separator:
        lines = [line + '\n' for line in lines]
    check_and_create_dir(file_path, print_msg=print_msg)
    file = open(file_path, mode='w', encoding='utf-8')
    file.writelines(lines)
    file.close()
    if print_msg:
        print('写入完成' + file_path)


def check_and_create_dir(file_path, print_msg=True):
    """
    检查并创建文件夹
    :param file_path: 要检查的文件路径，可以是文件也可以是文件夹
    :param print_msg: 是否显示消息
    :return:
    """
    if os.path.isdir(file_path):
        dir_name = file_path
    else:
        dir_name = os.path.dirname(file_path)
    if dir_name != '' and not os.path.exists(dir_name):
        if print_msg:
            print('创建' + dir_name)
        os.makedirs(dir_name)


def get_dict_from_file(file_path, separator='='):
    """
    从文件中读取字典，
    :param file_path:文件路径
    :param separator:分隔符
    :return: 如果有错返回None
    """
    result = dict()
    lines = read_lines(file_path)
    if lines is None:
        return None

    for line in lines:
        line = line.replace('\n', '')
        if separator in line:
            key_value = line.split(separator, maxsplit=1)
            result[key_value[0]] = key_value[1]
    return result


def get_result_file_name(source_file_name, suffix, extension=None):
    """
    获取结果文件名
    :param source_file_name: 
    :param suffix: 添加的后辍 
    :param extension:扩展名
    :return: 
    """
    name_suffix = os.path.splitext(source_file_name)
    if extension is None:
        extension = name_suffix[1]
    else:
        if not extension.startswith('.'):
            extension = '.' + extension
    result_file = '%s%s%s' % (name_suffix[0], suffix, extension)
    return result_file
