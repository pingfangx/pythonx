import re
from typing import List

from xx import filex
from xx import iox


class FileUtils:
    """文件工具"""

    def __init__(self):
        self.is_rfc = True

    def main(self):
        file = r"ignore/rfc793.txt"
        action_list = [
            ['退出', exit],
            ['处理文件换行用来方便翻译', self.process_line_break_for_translation, file],
        ]
        iox.choose_action(action_list)

    def process_line_break_for_translation(self, file, output=None):
        """处理文件换行"""
        if output is None:
            output = filex.get_result_file_name(file, '_line')
        ans = []
        lines = filex.read_lines(file, ignore_line_separator=True)
        if not lines:
            print(f'文件内容为空：{file}')
            exit()
        n = len(lines)
        i = 0
        while i < n:
            line = lines[i]
            print(f'{i} {line}')
            if self.need_inline(i, line, ans):
                print(f'{i} 行符合合并规则，尝试连接到上一行 {ans[-1]}')
                self.inline(line, ans)
            else:
                ans.append(line)
            i += 1
        filex.write_lines(output, ans, add_line_separator=True)

    def need_inline(self, i: int, line: str, lines: List[str]) -> bool:
        """是否需要合并到上一行"""
        if i <= 0:
            return False
        origin_line = line
        line = line.lstrip()
        if not line:
            return False
        pre_line = lines[-1].strip()
        if not pre_line:
            return False
        if '|' in line:  # rfc 中可能表示为图表
            return False
        first_char = line[0]
        if first_char.islower():  # 该行以小写开头，说明应该拼接到上一行
            return True
        elif first_char == '(':  # 括号也可以合并到上一行
            return True
        elif self.ends_with_article(pre_line):  # 虽然以大写结尾，但是前一行末尾是冠词
            return True
        elif self.is_rfc:
            # 是大写，但是可能是部分名词大写，也需要内联
            if not self.ends_with_end_symbol(pre_line):  # 不以结束符号结尾
                pre_line_leading_space = len(lines[-1]) - len(lines[-1].lstrip())
                line_leading_space = len(origin_line) - len(origin_line.lstrip())
                if line_leading_space >= pre_line_leading_space and line_leading_space > 0:
                    # 在 rfc 的情况下，如果是换行会有一个空行，如果没有空行，可以猜测应该需要拼接
                    first_word = re.split('[ ,]', line)[0]
                    if first_word in self.get_all_upper_words():
                        if not re.match(r'^\d{2,}', pre_line):  # 不以连续数字开头，在某些地方作为标题，后跟 requirement 不需要合并
                            return True
        return False

    @staticmethod
    def ends_with_article(line: str) -> bool:
        """是否以冠词结尾，如果上一行以冠词结尾，说明下一行的大写开头应该是专有名词，如
        The
        TCP ....
        """
        article_list = [
            'the',
            'a',
            'an'
        ]
        line = line.rstrip().lower()
        for article in article_list:
            if line.endswith(' ' + article.lower()):
                return True
        return False

    @staticmethod
    def ends_with_end_symbol(line: str) -> bool:
        """是否以结束符号结尾"""
        return line.endswith(('.', '?', '!'))

    @staticmethod
    def get_all_upper_words():
        """
        获取全部是大写的词
        包括部分 requirement 及专有名词
        """
        return [
            'MUST',
            'SHOULD',
            'NOT',
            'HTTP',
        ]

    @staticmethod
    def inline(line: str, lines: List[str]):
        line = line.lstrip()
        if lines[-1].endswith('-'):  # 以连字符结尾不需要额外添加空格
            lines[-1] += line
        else:
            lines[-1] += ' ' + line


if __name__ == '__main__':
    FileUtils().main()
