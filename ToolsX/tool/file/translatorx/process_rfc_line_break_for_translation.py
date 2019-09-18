import re
from typing import List

from xx import filex


class NextLine:
    def __init__(self, index: int, line: str, pre_index: int, pre_line: str, new_page: bool):
        self.index = index
        self.line = line
        self.pre_index = pre_index
        self.pre_line = pre_line
        self.new_page = new_page

    def valid(self):
        return self.index != -1


class FileUtils:
    """文件工具"""

    def __init__(self, file: str, output: str = None, start_line=None, end_line=None):
        self.file = file
        self.output = output
        if self.output is None:
            self.output = filex.get_result_file_name(self.file, '_line')

        self.start_line = start_line
        """起始行，用于只处理部分内容"""

        self.end_line = end_line
        """结束行，一般最后的致谢等内容不需要处理，需要过滤"""

    def start(self):
        lines = filex.read_lines(self.file, ignore_line_separator=True)
        if not lines:
            print(f'文件内容为空：{self.file}')
            return

        next_line = self.get_next_line(lines, 0)
        while next_line.valid():
            print(f'处理第 {next_line.index + 1} 行【{next_line.line}】')
            if self.need_inline(next_line):
                self.inline(lines, next_line)
                next_line = self.get_next_line(lines, next_line.pre_index)  # 从 pre 开始找
            else:
                next_line = self.get_next_line(lines, next_line.index)  # 从 index 开始找
        print(f'处理完毕，写入结果')
        filex.write_lines(self.output, lines, add_line_separator=True)

    def get_next_line(self, lines: List[str], pre_index: int) -> NextLine:
        """读取下一行"""
        n = len(lines)
        i = pre_index + 1  # 从起始行的下一行开始

        index = -1
        new_page = False

        while i < n:
            if i + 1 < n and lines[i + 1] == '\f':
                new_page = True
                print(f'第 {i + 2} 行翻页')
                i += 3  # 页尾，翻页，页眉，到达下一行
                continue
            line = lines[i]
            if self.start_line:  # 有起始行
                if self.start_line == line or re.fullmatch(self.start_line, line):
                    print(f'找到起始行，第 {i + 1} 行【{line}】')
                    self.start_line = None  # 置空，避免使用 flag
                else:
                    i += 1
                    continue
            if line and line.strip():
                if self.end_line is not None:  # 结束行
                    if self.end_line == line or re.fullmatch(self.end_line, line):
                        print(f'结束行【{line}】')
                        break
                    else:
                        index = i
                        break
                else:
                    index = i
                    break
            else:
                i += 1
        return NextLine(index, '' if index == -1 else lines[index], pre_index, lines[pre_index], new_page)

    def need_inline(self, next_line: NextLine) -> bool:
        """是否需要合并"""
        line = next_line.line
        pre_index = next_line.pre_index
        pre_line = next_line.pre_line

        inline = False
        space_count = len(line) - len(line.lstrip())
        if space_count == 0:
            print(f'缩进为 0，认为是独立行')
        elif space_count % 3 != 0:
            print(f'缩进是 {space_count} 认为不是文字行')
        elif space_count < self.get_space_count(pre_line):  # 正常情部分缩进应该大于等于上一行的缩过才能合并
            print(f'缩进是 {space_count} 小于上一行的缩进')
        elif self.is_assignment(line) or self.is_assignment(pre_line):
            print(f'是声明语句')
        elif line.lstrip().startswith('if') or pre_line.lstrip().startswith('if'):
            print(f'包含 if 可能是代码行')
        elif self.has_special_char(line):
            print(f'认为有特殊字符')
        elif self.ends_with_end_symbol(pre_line):
            print(f'前一行以结束符号结尾，认为已换行')
        elif self.is_title(pre_line):
            print(f'前一行是标题')
        elif re.search(r'\.{2,}\d+$', line):
            print(f'以 . 和数字结尾，认为是目录')
        else:
            first_char = line.lstrip()[0]
            first_word = re.split('[ ,]', line.lstrip())[0]
            if first_char.islower():  # 小写，一般需要合并，但有例外
                if first_char in '-' or first_word.endswith(':'):
                    print(f'{inline} 以特殊字符开头，不需要合并')
                else:
                    inline = True
                    print(f'{inline} 以小写字母开头')
            else:  # 以大写开头（实际是非小写开头，包含符号），一般不需要合并，但有例外
                if first_char in '"':
                    inline = True
                    print(f'{inline} 以 {first_char} 开头')
                elif self.ends_with_article(pre_line):
                    inline = True
                    print(f'{inline} 前一行以冠词或介词结尾')
                elif first_word.startswith('(Section'):
                    inline = True
                    print(f'{inline} 以特殊单词开头')
                elif first_word in self.get_all_proper_noun():
                    if not re.match(r'^\d{2,}', pre_line):
                        inline = True
                        print(f'{inline} 以大写字母开头，但可能是专有名词')
                    else:
                        print(f'{inline} 是标题')
                else:
                    print(f'{inline} 以大写字母开头')
        if not inline:
            print(f'不需要合并')
        return inline

    def inline(self, lines: List[str], next_line: NextLine):
        """合并行"""
        index = next_line.index
        pre_index = next_line.pre_index
        if not lines[pre_index].endswith('-'):  # 连字符不需要在拼接空格
            lines[pre_index] += ' '
        lines[pre_index] += lines[index].lstrip()  # 拼接
        lines[index] = ''  # 置空

    @staticmethod
    def get_space_count(line: str):
        return len(line) - len(line.lstrip())

    @staticmethod
    def is_assignment(line: str):
        """是否是类似赋值的语名"""
        return re.search('.+?=.+?', line)

    @staticmethod
    def ends_with_article(line: str) -> bool:
        """是否以冠词(或介词)结尾，如果上一行以冠词结尾，说明下一行的大写开头应该是专有名词，如
        The
        TCP ....
        """
        article_list = [
            'the',
            'a',
            'an',
            'in',
            'of',
            'and',
        ]
        line = line.rstrip().lower()
        for article in article_list:
            if line.endswith(' ' + article.lower()):
                return True
        return False

    @staticmethod
    def ends_with_end_symbol(line: str) -> bool:
        """是否以结束符号结尾"""
        return line[-1] in '.?!:;{}'

    @staticmethod
    def is_title(line: str) -> bool:
        """是否是标题"""
        return True if re.match(r'^(\d\.)+\s+\w', line) else False

    @staticmethod
    def get_all_proper_noun():
        """
        获取专有名词
        包括部分 requirement 及专有名词
        """
        return [
            'MAY',
            'SHOULD',
            'MUST',
            'NOT',
            'HTTP',
            'TLS',
            'Appendix',
        ]

    @staticmethod
    def has_special_char(line: str):
        """是否有特殊字符"""
        special_char = [
            '|',
            '+--',
            '{',
        ]
        for s in special_char:
            if s in line:
                return True
        return False


if __name__ == '__main__':
    FileUtils(
        r'ignore/rfc8446.txt',
        end_line=r'^\d.*Acknowledgements$'
    ).start()
