import re

from xx import iox, filex


class ProcessLog:
    """处理日志"""

    def main(self):
        action_list = [
            ['退出', exit],
            ['过滤日志', self.filter_log],
        ]
        iox.choose_action(action_list)

    def filter_log(self, log_file):
        lines = filex.read_lines(log_file)
        print(f'日志 {len(lines)} 行')
        lines = list(filter(self.filter_line, lines))
        print(f'过滤后 {len(lines)} 行')
        filex.write_lines(filex.get_result_file_name(log_file, '_result'), lines)

    @staticmethod
    def filter_line(line):
        pattern = re.compile(r'(/xx/xxtieba|[sS]pider|data/|static/|\.ico|robots)')
        if re.search(pattern, line):
            return False
        return True


if __name__ == '__main__':
    ProcessLog().filter_log('ignore/access_20181109.log')
