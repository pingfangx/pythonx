import math
import os.path
import re
from configparser import ConfigParser


def read(file_path, encoding='utf-8'):
    """读取文件内容"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, encoding=encoding) as f:
        return f.read()


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
            result = [line.rstrip('\n') for line in f.readlines()]
        else:
            result = f.readlines()
    return result


def write_lines(file_path, lines, mode='w', encoding='utf-8', add_line_separator=False, print_msg=True):
    """
    写入翻译结果
    :param file_path: 要写入的文件
    :param lines: 结果数组
    :param mode: 写入模式
    :param encoding: 编码
    :param add_line_separator: 是否添加换行符
    :param print_msg: 是否显示
    :return: 
    """
    if add_line_separator:
        lines = [line + '\n' for line in lines]
    check_and_create_dir(file_path, print_msg=print_msg)
    file = open(file_path, mode=mode, encoding=encoding)
    file.writelines(lines)
    file.close()
    if print_msg:
        print('写入完成' + file_path)


def write(file_path, content, mode='w', encoding='utf-8', print_msg=True):
    """直接写入内容"""
    check_and_create_dir(file_path, print_msg=print_msg)
    file = open(file_path, mode=mode, encoding=encoding)
    file.write(content)
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


def get_dict_from_file(file_path, separator='=', join_line=True):
    """
    从文件中读取字典，
    :param file_path:文件路径
    :param separator:分隔符
    :param join_line: 是否连接行
    :return: 如果有错返回None
    """
    result = dict()
    lines = read_lines(file_path)
    if lines is None:
        return None

    pre_line = None
    for line in lines:
        line = line.replace('\n', '')
        if join_line:
            if pre_line is not None:
                # 连接前一行
                line = pre_line + line
            if line.endswith('\\'):
                # 在.properties文件中，有一些行会以\结尾，要求连接
                pre_line = line
                continue
            else:
                pre_line = None
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


def get_config(file_path, encoding='utf-8'):
    """
    读取配置
    :param file_path:配置文件 
    :param encoding: 编码
    :return: 
    """
    conf = ConfigParser()
    conf.read(file_path, encoding=encoding)
    return conf


def list_file(dir_path, name_pattern=None):
    """
    列出目录中的文件，返回文件路径的数组
    :param dir_path:目录，如果传一个文件，则会返回只包含该文件的数组
    :param name_pattern: 文件名的正则匹配
    :return:
    """
    file_list = list()
    if os.path.isfile(dir_path):
        file_list.append(dir_path)
    elif os.path.isdir(dir_path):
        for parent, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                if name_pattern is not None:
                    if re.search(name_pattern, file) is not None:
                        file_list.append(parent + '\\' + file)
                else:
                    file_list.append(parent + '\\' + file)
    return file_list


def get_file_size_str(file_path):
    """获取文件长度"""
    try:
        size = os.path.getsize(file_path)
        return parse_file_size(size)
    except OSError:
        return 'error'


def parse_file_size(size):
    """解析文件大小"""
    unit_array = ['B', 'K', 'M', 'G', 'T']
    if size < 0:
        return 'error'
    if size == 0:
        return '0B'
    i = int(math.log2(size) / math.log2(1024))
    if i >= len(unit_array):
        i = len(unit_array) - 1
    return f'{size/1024**i:#.2f}{unit_array[i]}'
