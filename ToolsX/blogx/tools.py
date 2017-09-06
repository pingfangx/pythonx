import re

import pyperclip

from xx import iox


class BlogXTools:
    DESTINATION_COPYRIGHT = '转载申明'
    DESTINATION_COPYRIGHT_AND_TITLE = '转载申明加标题'
    DESTINATION_URL = '网址'
    DESTINATION_QUOTE = '引用'
    DESTINATION_REFERENCE_AND_QUOTE = '参考文献和引用'

    PATTERN_CLIPBOARD = r'tid=(\d+)'
    PATTERN_URL = r'thread-(\d+)'

    def main(self):
        action_list = [
            ['退出', exit],
        ]
        destination_list = [
            BlogXTools.DESTINATION_COPYRIGHT,
            BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE,
            BlogXTools.DESTINATION_URL,
            BlogXTools.DESTINATION_QUOTE,
            BlogXTools.DESTINATION_REFERENCE_AND_QUOTE,
            ['外部链接转为参考文献和引用', self.parse_reference_and_quote]
        ]
        for destination in destination_list:
            if isinstance(destination, str):
                action = '→%s' % destination
                action_list.append([action, self.parse_text, destination])
            elif isinstance(destination, list):
                action = '→%s' % destination[0]
                action_list.append([action, self.parse_text, destination[1]])
        while True:
            iox.choose_action(action_list)

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
                url = 'http://blog.pingfangx.com/%s.html' % tid
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

        if result is not None:
            BlogXTools.copy_text(result)

    @staticmethod
    def get_title_and_tid(text):
        title = None
        tid = None
        lines = text.split('\n')
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


if __name__ == '__main__':
    BlogXTools().main()
