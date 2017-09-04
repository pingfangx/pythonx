import re

import pyperclip

from xx import iox


class BlogXTools:
    SOURCE_URL = '地址'
    SOURCE_CLIPBOARD = '剪贴板'

    DESTINATION_COPYRIGHT = '转载申明'
    DESTINATION_COPYRIGHT_AND_TITLE = '转载申明加标题'
    DESTINATION_URL = '网址'

    PATTERN_CLIPBOARD = r'tid=(\d+)'
    PATTERN_URL = r'thread-(\d+)'

    def main(self):
        action_list = [
            ['退出', exit],
        ]
        parse_action = [
            [BlogXTools.SOURCE_CLIPBOARD, BlogXTools.DESTINATION_COPYRIGHT],
            [BlogXTools.SOURCE_CLIPBOARD, BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE],
            [BlogXTools.SOURCE_CLIPBOARD, BlogXTools.DESTINATION_URL],
            [BlogXTools.SOURCE_URL, BlogXTools.DESTINATION_COPYRIGHT],
        ]
        for source, destination in parse_action:
            action = '%s→%s' % (source, destination)
            action_list.append([action, self.parse_text, source, destination])
        while True:
            iox.choose_action(action_list)

    @staticmethod
    def parse_text(source, destination, text=None):
        if text is None:
            text = pyperclip.paste()
        if text is None or text == '':
            print('请输入:\n')
            text = input()
        if source == BlogXTools.SOURCE_CLIPBOARD:
            pattern = BlogXTools.PATTERN_CLIPBOARD
        elif source == BlogXTools.SOURCE_URL:
            pattern = BlogXTools.PATTERN_URL
        else:
            pattern = ''
        if destination == BlogXTools.DESTINATION_COPYRIGHT or destination == BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE:
            if source == BlogXTools.SOURCE_CLIPBOARD:
                lines = text.split('\n')
                for i in range(len(lines)):
                    line = lines[i]
                    match = re.search(pattern, line)
                    if match is not None:
                        if destination == BlogXTools.DESTINATION_COPYRIGHT:
                            BlogXTools.parse_text_to_copyright(pattern, line)
                        elif destination == BlogXTools.DESTINATION_COPYRIGHT_AND_TITLE:
                            title = lines[i - 1]
                            tid = match.group(1)
                            url = 'http://blog.pingfangx.com/%s.html' % tid
                            result = '# %s\n>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (title, url, url)
                            pyperclip.copy(result)
                            print('已复制：\n\n' + result)
                        break
            else:
                BlogXTools.parse_text_to_copyright(pattern, text)
        elif destination == BlogXTools.DESTINATION_URL:
            BlogXTools.parse_text_to_url(pattern, text)

    @staticmethod
    def parse_text_to_url(pattern, text):
        lines = text.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            match = re.search(pattern, line)
            if match is not None:
                title = lines[i - 1].strip()
                tid = match.group(1)
                url = 'http://blog.pingfangx.com/%s.html' % tid
                result = '[%s](%s)' % (title, url)
                pyperclip.copy(result)
                print('已复制：\n\n' + result)
                break

    @staticmethod
    def parse_text_to_copyright(pattern, text):
        match = re.search(pattern, text)
        if match is not None:
            tid = match.group(1)
            url = 'http://blog.pingfangx.com/%s.html' % tid
            result = '>本文由平方X发表于平方X网，转载请注明出处。[%s](%s)\n\n' % (url, url)
            pyperclip.copy(result)
            print('已复制：\n\n' + result)


if __name__ == '__main__':
    BlogXTools().main()
