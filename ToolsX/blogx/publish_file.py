import os
import sys

import pyperclip

sys.path.append("..")
from xx import filex
from xx import iox


class BlogXTools:
    def __init__(self):
        self.process_file = r'D:\workspace\BlogX\CodeFarmer\git\usages\git 移动一个提交.txt'
        self.add_note = False
        self.tid = ''

    def main(self):
        action_list = [
            ['退出', exit],
            ['自动处理文件', self.process, self.process_file, self.tid],
            ['设置处理文件', self.set_process_file],
            ['手动设置 tid', self.set_tid],
            ['切换添加转载申明', self.toggle_add_note],
        ]
        print('\n2-当前处理的文件是 %s\n3-tid=%s\n4-添加转载申明 %s' % (self.process_file, self.tid, self.add_note))
        iox.choose_action(action_list)

    def set_process_file(self):
        """设置处理的文件"""
        input_file = input('请输入或拖入要处理的文件或文件夹\n')
        if not input_file:
            print('没有输入')
        input_file = input_file.strip('"')
        if os.path.isfile(input_file):
            self.process_file = input_file
        self.main()

    def toggle_add_note(self):
        """切换是否添加转载申明"""
        self.add_note = not self.add_note
        self.main()

    def set_tid(self):
        """手动设置 tid"""
        input_tid = input('请输入 tid\n')
        if not input_tid:
            print('没有输入')
        else:
            self.tid = input_tid
        self.main()

    def process(self, file_path, tid):
        """处理文件"""
        folder, file_name = os.path.split(file_path)
        title = os.path.splitext(file_name)[0]
        new_name = '[%s]%s.md' % (tid, title)
        new_path = folder + os.path.sep + new_name
        if file_name != new_name:
            print('%s → %s' % (file_path, new_path))
            os.rename(file_path, new_path)

        print('处理文件%s' % new_path)
        lines = filex.read_lines(new_path)
        first_line = lines[0]
        need_process = True
        if first_line.startswith('[md]'):
            print('第一行已经包含[md]标签，不处理')
            need_process = False
        elif first_line.startswith('>本文由平方X'):
            print('第一行已经包含转载申明')
        else:
            if self.add_note:
                # 添加转载申明
                url = 'http://blog.pingfangx.com/%s.html' % tid
                result = '>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (url, url)
                lines.insert(0, result)
                print('已写入转载申明')
        if need_process:
            # 写入[md]标签
            lines.insert(0, '[md]\n\n')
            lines.append('\n\n[/md]')
            filex.write_lines(new_path, lines)
        # 复制
        text = ''.join(lines)
        post_title = '[%s]%s' % (tid, title)
        self.post_blog(post_title, text)
        self.copy_text(text, False)

    @staticmethod
    def copy_text(text, print_msg=True):
        """复制文本"""
        pyperclip.copy(text)
        if print_msg:
            print('已复制：\n' + text)

    def post_blog(self, title, text):
        """将博客发布"""
        print('发布%s' % title)
        pass


if __name__ == '__main__':
    BlogXTools().main()
