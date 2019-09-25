import os
from typing import List

import xmind
from xmind.core.sheet import SheetElement
from xmind.core.topic import TopicElement
from xmind.core.workbook import WorkbookDocument

from xx import filex


class XmindIndentUtils:

    def __init__(self, xmind_file_path, indent_output=None):
        self.xmind_file_path = xmind_file_path
        """ xmind 文件"""
        self.indent_output = indent_output
        """缩进输出文件"""

    def print_workbook_as_indent(self):
        workbook = xmind.load(self.xmind_file_path)
        out_file = self.get_indent_out_file(workbook)
        lines = self.collect_sheet_as_indent(workbook.getPrimarySheet())
        filex.write_lines(out_file, lines, add_line_separator=True)

    def update_indent_file(self):
        workbook = xmind.load(self.xmind_file_path)
        out_file = self.get_indent_out_file(workbook)
        if not os.path.exists(out_file):
            print(f'{out_file} 不存在，直接写入')
            self.print_workbook_as_indent()
            return
        else:
            print(f'更新 {out_file}')
        old_lines = filex.read_lines(out_file, ignore_line_separator=True)
        new_lines = self.collect_sheet_as_indent(workbook.getPrimarySheet())
        for i, line in enumerate(old_lines):
            if line not in new_lines:
                print(f'需要插入行\n{line}')
                self.insert_line(i, old_lines, new_lines)
        filex.write_lines(out_file, new_lines, add_line_separator=True)

    @staticmethod
    def insert_line(index, old_lines, new_lines):
        """因为按顺序读取，直接取前一行"""
        line = old_lines[index]
        pre_line = ''
        if index > 0:
            pre_line = old_lines[index - 1]
        if not pre_line:
            print(f'没有找到前一行缩进')
        else:
            print(f'前一行为\n{pre_line}')
            count = new_lines.count(pre_line)
            if count == 0:
                print(f'没有找到，无法插入')
            elif count > 1:
                print(f'找到多行，无法插入')
            else:
                j = new_lines.index(pre_line)
                print(f'插入到第 {j} 行后')
                new_lines.insert(j + 1, line)

    def get_indent_out_file(self, workbook: WorkbookDocument):
        out_file = self.indent_output
        if not out_file:
            out_file = workbook.getPrimarySheet().getRootTopic().getTitle() + '.md'
        return out_file

    def collect_sheet_as_indent(self, sheet: SheetElement) -> List[str]:
        lines = []
        root_topic = sheet.getRootTopic()
        if not root_topic:
            return []
        self.collection_lines_as_indent(lines, root_topic)
        if not lines:
            return []
        lines[0] = '# ' + lines[0]
        return lines

    def collection_lines_as_indent(self, lines: List[str], topic: TopicElement, indent=''):
        lines.append(indent + topic.getTitle())
        indent += ' ' * 4
        for i in topic.getSubTopics():
            self.collection_lines_as_indent(lines, i, indent)
