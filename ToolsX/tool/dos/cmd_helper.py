from subprocess import call

import os
from xx import filex
from xx import iox


class CmdHelper:
    """
    windows 中的 cmd 的帮助
    相关博文:《dos 整理》(http://blog.pingfangx.com/2391.html)
    """

    def __init__(self):
        self.help_list_file = os.path.abspath('.') + '/data/cmd_list.txt'
        self.temp_file = os.path.abspath('.') + '/data/tmp.txt'
        self.all_cmd_file = os.path.abspath('.') + '/data/cmd_help.md'

    def main(self):
        action_list = [
            ['退出', exit],
            ['输出 help', self.export_help_list],
            ['输出各命令的 help', self.export_all_cmd_help],
        ]
        iox.choose_action(action_list)

    def export_help_list(self):
        """导出帮助"""
        cmd = 'help > %s' % self.help_list_file
        self.run_cmd(cmd)

    def export_all_cmd_help(self):
        """导出所有命令的帮助"""
        cmd_list = self.get_all_cmd()
        length = len(cmd_list)
        for i in range(length):
            print('%d/%d' % (i + 1, length))
            cmd = cmd_list[i]
            if ' ' not in cmd:
                continue
            cmd, info = cmd.split(' ', maxsplit=1)
            filex.write(self.all_cmd_file, '\n\n# 【%d/%d】%s\n' % (i + 1, length, cmd), mode='a')
            if cmd == 'SC':
                # 这个要输入，卡住了
                continue
            cmd = 'help %s > %s' % (cmd, self.temp_file)
            self.run_cmd(cmd)
            result = filex.read_lines(self.temp_file, encoding='gbk')
            result.insert(0, '```\n')
            result.append('\n```')
            filex.write_lines(self.all_cmd_file, result, mode='a')
        os.remove(self.temp_file)

    def get_all_cmd(self):
        """获取 help 输出的所有命令，处理换行"""
        lines = filex.read_lines(self.help_list_file, encoding='gbk', ignore_line_separator=True)
        result = list()
        for i in range(1, len(lines)):
            line = lines[i]
            if line.startswith(' '):
                result[-1] += line.lstrip()
            else:
                if ' ' in line:
                    result.append(line)
        return result

    @staticmethod
    def run_cmd(cmd):
        print(cmd)
        call(cmd, shell=True)


if __name__ == '__main__':
    CmdHelper().main()
