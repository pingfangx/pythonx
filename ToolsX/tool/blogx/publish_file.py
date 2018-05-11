import locale
import os
import sys

import pyperclip
import requests

sys.path.append("../..")
from xx import netx
from xx import filex
from xx import iox


class BlogXTools:
    def __init__(self, cookies):
        self.cookies = cookies
        self.file_path = ''
        self.add_note = False
        self.add_md_in_file = False
        """是否在文件中添加 md 标签，置为 false 在发布时再添加"""
        self.fid = 56
        """论动 id ，这个以后可以修改为通过文件名判断"""
        self.tid = 0
        self.tid_file = 'ignore/tid.txt'

    def main(self):
        action_list = [
            ['退出', exit],
            ['设置处理文件', self.set_file_path],
            ['自动获取 tid', self.get_tid_from_net],
            ['处理文件', self.process_file],
            ['发布', self.post_blog],
            ['编辑', self.edit_blog],
            ['手动设置 fid', self.set_fid],
            ['手动设置 tid', self.set_tid],
            ['切换添加转载申明', self.toggle_add_note],
        ]
        self.read_tid()
        while True:
            print('\nfile_path=%s' % self.file_path)
            print('fid=%s' % self.fid)
            print('tid=%s' % self.tid)
            print('add_note=%s' % self.add_note)
            print('add_md_in_file=%s' % self.add_md_in_file)
            iox.choose_action(action_list)

    def set_file_path(self):
        """设置处理的文件"""
        input_file = input('请输入或拖入要处理的文件或文件夹\n')
        if not input_file:
            print('没有输入')
        input_file = input_file.strip('"')
        if os.path.isfile(input_file):
            self.file_path = input_file

    def toggle_add_note(self):
        """切换是否添加转载申明"""
        self.add_note = not self.add_note

    def set_fid(self):
        """手动设置 fid"""
        input_fid = input('请输入 fid\n')
        if not input_fid:
            print('没有输入')
        else:
            self.fid = input_fid

    def set_tid(self):
        """手动设置 tid"""
        input_tid = input('请输入 tid\n')
        if not input_tid:
            print('没有输入')
        else:
            self.tid = int(input_tid)
            self.save_tid()

    def read_tid(self):
        if os.path.exists(self.tid_file):
            with open(self.tid_file, mode='r', encoding='utf-8') as f:
                self.tid = int(f.read())

    def save_tid(self):
        with open(self.tid_file, mode='w', encoding='utf-8') as f:
            f.write(str(self.tid))
            print('已将 tid 设置为 %s ' % self.tid)

    def get_tid_from_net(self):
        """获取 tid"""
        url = 'http://www.pingfangx.com/xx/blog/api/get_last_tid'
        last_tid = netx.handle_result(requests.get(url, cookies=self.cookies))
        if last_tid:
            self.tid = last_tid + 1
            self.save_tid()

    def process_file(self):
        """处理文件"""
        folder, file_name = os.path.split(self.file_path)
        title = os.path.splitext(file_name)[0]
        if title.startswith('[%s]' % self.tid):
            new_name = title + '.md'
        else:
            new_name = '[%s]%s.md' % (self.tid, title)
        new_path = folder + os.path.sep + new_name
        if file_name != new_name:
            print('%s → %s' % (self.file_path, new_path))
            os.rename(self.file_path, new_path)
            self.file_path = new_path
            print('已将 file_path 置为 %s' % self.file_path)

        print('处理文件%s' % new_path)
        try:
            lines = filex.read_lines(new_path)
        except UnicodeDecodeError:
            lines = filex.read_lines(new_path, encoding=locale.getpreferredencoding(False))
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
                url = 'http://blog.pingfangx.com/%s.html' % self.tid
                result = '>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (url, url)
                lines.insert(0, result)
                print('已写入转载申明')
        if need_process:
            # 写入[md]标签
            if self.add_md_in_file:
                lines.insert(0, '[md]\n\n')
                lines.append('\n\n[/md]')
        filex.write_lines(new_path, lines)

    @staticmethod
    def copy_text(text, print_msg=True):
        """复制文本"""
        pyperclip.copy(text)
        if print_msg:
            print('已复制：\n' + text)

    def read_blog(self):
        base_name = os.path.basename(self.file_path)
        title = os.path.splitext(base_name)[0]
        with open(self.file_path, encoding='utf-8') as f:
            content = f.read()
        if not content:
            print('没有读取到内容')
            return None, None
        if not content.startswith('[md]'):
            content = '[md]\n' + content
        if not content.endswith('[/md]'):
            content += '[/md]'
        return title, content

    def post_blog(self):
        """将博客发布"""
        title, content = self.read_blog()
        print('发布%s' % title)
        data = {
            'fid': self.fid,
            'title': title,
            'content': content
        }
        url = 'http://www.pingfangx.com/xx/blog/api/post'
        success_tid = netx.handle_result(requests.post(url, data, cookies=self.cookies))
        if success_tid:
            success_tid = int(success_tid)
            if success_tid == self.tid:
                print('发帖成功 tid 正常')
            else:
                print('tid 不正常，可能需要手动修改 %s-%s' % (self.tid, success_tid))
            self.tid = success_tid + 1
            self.save_tid()

    def edit_blog(self):
        """编辑博客"""
        title, content = self.read_blog()
        print('编辑%s' % title)
        data = {
            'title': title,
            'content': content
        }
        url = 'http://www.pingfangx.com/xx/blog/api/edit'
        success_tid = netx.handle_result(requests.post(url, data, cookies=self.cookies))
        if success_tid:
            print('编辑成功')


if __name__ == '__main__':
    cookie_file = 'ignore/cookies.txt'
    if not os.path.exists(cookie_file):
        print('文件不存在 %s' % cookie_file)
        exit()
    with open(cookie_file, encoding='utf-8') as f:
        cookies_str = f.read()
        BlogXTools(netx.parse_cookies(cookies_str)).main()
