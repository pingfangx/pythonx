import os.path


def read_lines(file_path):
    """
    读取所有行
    :param file_path: 
    :return: 
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, encoding='utf-8') as f:
        result = f.readlines()
    return result


def write_lines(file_path, lines, print_msg=True):
    """
    写入翻译结果
    :param file_path: 要写入的文件
    :param lines: 结果数组
    :param print_msg: 是否显示
    :return: 
    """
    file = open(file_path, mode='w', encoding='utf-8')
    file.writelines(lines)
    file.close()
    if print_msg:
        print('写入完成' + file_path)


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
