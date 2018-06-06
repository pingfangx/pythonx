import os
import re
import sys

import pyperclip

sys.path.append("../..")
from xx import filex
from xx import iox


class BlogXTools:
    DESTINATION_COPYRIGHT = '转载申明'
    DESTINATION_COPYRIGHT_AND_TITLE = '转载申明加标题'
    DESTINATION_URL = '标题和网址'
    DESTINATION_QUOTE = '引用'
    DESTINATION_REFERENCE_AND_QUOTE = '参考文献和引用'
    DESTINATION_FILE_NAME_WITH_ID = '文件名带id'
    RELATIVE_BLOG = '相关博文'

    PATTERN_CLIPBOARD = r'tid=(\d+)'
    PATTERN_URL = r'thread-(\d+)'

    process_dir = r'D:\workspace\BlogX\draft'

    def main(self):
        action_list = [
            ['退出', exit],
            ['设置处理目录', self.set_process_dir],
        ]
        destination_list = [
            BlogXTools.DESTINATION_COPYRIGHT,
            BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE,
            BlogXTools.DESTINATION_URL,
            BlogXTools.DESTINATION_QUOTE,
            BlogXTools.DESTINATION_REFERENCE_AND_QUOTE,
            BlogXTools.DESTINATION_FILE_NAME_WITH_ID,
            BlogXTools.RELATIVE_BLOG,
            ['外部链接转为地址', self.parse_reference],
            ['外部链接转为参考文献和引用', self.parse_reference_and_quote],
            ['通过标题重命名文件、添加[md]标签', self.auto_process_file],
            ['通过标题重命名文件、添加转载申明、添加[md]标签', self.auto_process_file2]
        ]
        for destination in destination_list:
            if isinstance(destination, str):
                action = '→%s' % destination
                action_list.append([action, self.parse_text, destination])
            elif isinstance(destination, list):
                action = '→%s' % destination[0]
                action_list.append([action, self.parse_text, destination[1]])
        print('\n当前处理的文件夹是 %s' % BlogXTools.process_dir)
        iox.choose_action(action_list)

    def set_process_dir(self):
        """设置处理的文件"""
        input_file = input('请输入或拖入要处理的文件或文件夹\n')
        if not input_file:
            print('没有输入')
        input_file = input_file.strip('"')
        if os.path.isdir(input_file):
            BlogXTools.process_dir = input_file
        elif os.path.isfile(input_file):
            BlogXTools.process_dir = os.path.dirname(input_file)
        self.main()

    @staticmethod
    def parse_text(destination, text=None):
        result = None
        if text is None:
            text = pyperclip.paste()
        if text is None or text == '':
            print('请输入:\n')
            text = input()

        if callable(destination):
            result = destination(text)
        elif isinstance(destination, str):
            title, tid = BlogXTools.get_title_and_tid(text)
            if tid is not None:
                url = 'https://www.pingfangx.com/blog/%s' % tid
                if destination == BlogXTools.DESTINATION_COPYRIGHT:
                    result = '>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (url, url)
                elif destination == BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE:
                    result = '# %s\n>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (title, url, url)
                elif destination == BlogXTools.DESTINATION_URL:
                    result = '[%s](%s)' % (title, url)
                elif destination == BlogXTools.DESTINATION_QUOTE:
                    result = '[1]:%s "%s"' % (url, title)
                elif destination == BlogXTools.DESTINATION_REFERENCE_AND_QUOTE:
                    result = '[[1]].[%s](%s)  \n[1]:%s "%s"' % (title, url, url, title)
                elif destination == BlogXTools.DESTINATION_FILE_NAME_WITH_ID:
                    result = '[%s]%s' % (tid, title)
                elif destination == BlogXTools.RELATIVE_BLOG:
                    result = '相关博文:[《%s》](%s)' % (title, url)

        if result is not None:
            BlogXTools.copy_text(result)

    @staticmethod
    def get_title_and_tid(text):
        title = None
        tid = None
        lines = text.split('\n')
        if len(lines) == 1:
            line = lines[0]
            # (.*?) 的懒惰必须配合结尾的 $ ，否则就匹配空了
            # 如果不懒惰则会包含后面的 .md，?判断无效
            match = re.match(r'\[(\d+)](.*?)(\.(md)|(txt))?$', line)
            if match:
                return match.group(2), match.group(1)
        for i in range(len(lines)):
            line = lines[i]
            tid = BlogXTools.get_tid(line)
            if tid is not None:
                if i > 0:
                    title = lines[i - 1].strip()
                break
        return title, tid

    @staticmethod
    def get_tid(text):
        """获取网址中的tid"""
        match = re.search(BlogXTools.PATTERN_URL, text)
        if match is None:
            match = re.search(BlogXTools.PATTERN_CLIPBOARD, text)
        if match is not None:
            return match.group(1)
        return None

    @staticmethod
    def copy_text(text, print_msg=True):
        """复制文本"""
        pyperclip.copy(text)
        if print_msg:
            print('已复制：\n' + text)

    @staticmethod
    def parse_reference(text):
        """解析外部链接为地址
        格式为：
        作者
        标题
        地址
        """
        lines = text.split('\n')
        lines = [line.replace('\r', '') for line in lines]
        reference = ''
        for i in range(len(lines)):
            line = lines[i]
            if line:
                author, title, url = lines[i:i + 3]
                reference = '\n[%s.《%s》](%s)  ' % (author, title, url)
                break
        return reference

    @staticmethod
    def parse_reference_and_quote(text):
        """
        解析为参考文献和引用
        格式为：
        序号
        作者
        标题
        地址
        """
        lines = text.split('\n')
        lines = [line.replace('\r', '') for line in lines]
        reference = ''
        quote = ''
        for i in range(len(lines)):
            line = lines[i]
            if re.match('\d', line):
                # 是序号
                if i + 3 < len(lines):
                    index, author, title, url = lines[i:i + 4]
                    reference += '\n[[%s]].[%s.《%s》](%s)  ' % (index, author, title, url)
                    quote += '\n[%s]:%s (%s.《%s》)' % (index, url, author, title)
                    i += 3
        return reference + '\n' + quote

    @staticmethod
    def auto_process_file(text):
        return BlogXTools.auto_process_file2(text, False)

    @staticmethod
    def auto_process_file2(text, add_note=True):
        """
        自动处理文件
        :param text: 从 discuz 复制的文本
        :param add_note: 是否添加转截申明
        :return: 
        """
        title, tid = BlogXTools.get_title_and_tid(text)
        if tid is not None:
            file_name = '[%s]%s.md' % (tid, title)
            found_file = None
            for file in filex.list_file(BlogXTools.process_dir):
                parent_dir, base_name = os.path.split(file)
                if base_name == file_name:
                    print('打到文件')
                    found_file = file
                    break
                elif base_name == '%s.txt' % title:
                    print('找到未命名的文件，执行重命名')
                    new_name = parent_dir + '/' + file_name
                    os.rename(file, new_name)
                    found_file = new_name
                    break
            if found_file:
                lines = filex.read_lines(found_file)
                first_line = lines[0]
                need_process = True
                if first_line.startswith('[md]'):
                    print('第一行已经包含[md]标签，不处理')
                    need_process = False
                elif first_line.startswith('>本文由平方X'):
                    print('第一行已经包含转载申明')
                else:
                    if add_note:
                        # 添加转载申明
                        url = 'http://blog.pingfangx.com/%s.html' % tid
                        result = '>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (url, url)
                        lines.insert(0, result)
                        print('已写入转载申明')
                if need_process:
                    # 写入[md]标签
                    lines.insert(0, '[md]\n\n')
                    lines.append('\n\n[/md]')
                    filex.write_lines(found_file, lines)
                # 复制
                text = ''.join(lines)

        return text


if __name__ == '__main__':
    BlogXTools().main()
