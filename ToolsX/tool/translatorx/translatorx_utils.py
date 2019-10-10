import datetime
from typing import Dict
from xml.etree import ElementTree as Et

import common_utils

"""
与翻译相关的工具
"""


def get_translation_dict_from_file(file_path, separator='=', join_line=True) -> Dict:
    """从文件中读取翻译字典

    :param file_path:文件路径
    :param separator:分隔符
    :param join_line: 是否连接行
    :return: 如果有错返回None
    """
    result = dict()
    lines = common_utils.read_lines(file_path)
    if lines is None:
        return {}

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
            k, v = line.split(separator, maxsplit=1)
            result[k] = v
    return result


def get_translation_dict_from_omegat_file(file_path) -> dict:
    """读取 omegat 的记忆文件"""
    tree = Et.parse(file_path)
    tmx = tree.getroot()
    body = tmx.find('body')
    result = dict()
    for tu in body.iter('tu'):
        cn = None
        en = None
        for tuv in tu.iter('tuv'):
            lang = tuv.attrib['lang'].upper()
            if lang == 'EN-US':
                en = tuv.find('seg').text
            elif lang == 'ZH-CN':
                cn = tuv.find('seg').text
        if en is not None:
            # 中文允许为空
            result[en] = cn
    return result


def save_translation_dict_to_omegat_file(translation_dict: Dict, output_file):
    """保存翻译"""
    tmx = Et.Element('tmx')
    tmx.attrib['version'] = '1.1'
    Et.SubElement(tmx, 'header')
    body = Et.SubElement(tmx, 'body')
    for (k, v) in translation_dict.items():
        if v:
            # 只添加不为空的
            _add_translate_element(body, k, v)

    tree = Et.ElementTree(tmx)
    tree.write(output_file, encoding='utf-8')
    print('输出为' + output_file)


def _add_translate_element(element, en: str, cn: str):
    """向element中添加一个翻译"""

    tu = Et.SubElement(element, 'tu')
    # 英文
    tuv = Et.SubElement(tu, 'tuv')
    tuv.attrib['lang'] = 'EN-US'
    seg = Et.SubElement(tuv, 'seg')
    seg.text = en.strip()
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
    seg2.text = cn.strip()


def unicode_str_to_chinese(unicode_str):
    """unicode 的 str 转为中文"""
    try:
        return unicode_str.encode().decode('unicode_escape')
    except UnicodeDecodeError:
        return unicode_str


def chinese_to_unicode(chinese_str):
    """中文转为 unicode"""
    try:
        return chinese_str.encode('unicode_escape').decode()
    except UnicodeEncodeError:
        return chinese_str
