"""
处理excel
"""
import datetime
import os

import xlrd
import xlwt
from xlutils.copy import copy


def open_or_create_workbook(file_path):
    """
    打开或创建工作薄
    :param file_path: 文件路径
    :return: 
    """
    if os.path.exists(file_path):
        read_workbook = xlrd.open_workbook(file_path)
        workbook = copy(read_workbook)
    else:
        workbook = xlwt.Workbook(encoding='utf-8')
        workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    return workbook


def read_from_excel(file_path, date_format='%Y-%m-%d'):
    """

    :param file_path: 文件路径
    :param date_format: 如果有时间时，格式化的日符串
    :return:
    """
    if not os.path.exists(file_path):
        return []
    read_book = xlrd.open_workbook(file_path)
    sheet = read_book.sheet_by_index(0)
    data = []
    for row in range(sheet.nrows):
        column = []
        for col in range(sheet.ncols):
            cell = sheet.cell(row, col)
            if cell.ctype == 3:
                date = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, 0))
                value = date.strftime(date_format)
            else:
                value = cell.value
            column.append(value)
        data.append(column)
    return data


def write_list_to_excel(file_path, data, title=None, separator='|', print_msg=True):
    """
    将数据写入
    :param file_path: 文件路径
    :param data: 数据
    :param title: 标题
    :param separator:分隔符 
    :param print_msg: 是否显示
    :return: 
    """
    workbook = open_or_create_workbook(file_path)
    sheet = workbook.get_sheet(0)
    delta_row = 0
    if title is not None and isinstance(title, list):
        delta_row = 1
        sheet = workbook.get_sheet(0)
        for i in range(len(title)):
            column = sheet.col(i)
            # 可以设置宽度
            # column.width = 256 * 100
            sheet.write(0, i, title[i])
    for i in range(len(data)):
        row = data[i]
        if isinstance(row, list):
            cells = row
        else:
            cells = row.split(separator)
        for j in range(len(cells)):
            sheet.write(i + delta_row, j, cells[j])
    workbook.save(file_path)
    if print_msg:
        print('写入完成' + file_path)
