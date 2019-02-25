import re

from xx import encodex
from xx import filex
from xx import iox


class KeymapReference:
    """
    AndroidStudio快捷键参考的处理
    [AndroidStudio翻译(5)-Keymap Refrence快捷键参考中文翻译](http://blog.pingfangx.com/2357.html)
    来自：https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf
    保存后将其复制出来，然后用“【”划分快捷键，再进行一次处理
    """

    def main(self):

        # 快捷键参考
        keymap_reference_file = 'data/IntelliJIDEA_ReferenceCard.txt'
        keymap_reference_translation_file = r'D:\workspace\TranslatorX\AndroidStudio\target' \
                                            r'\IntelliJIDEA_ReferenceCard_modified_zh_CN.properties '

        action_list = [
            ['退出', exit],
            ['处理快捷键参考文件', self.process_keymap_reference_card, keymap_reference_file],
            ['处理快捷键参考文件的翻译结果', self.process_keymap_reference_card_translation, keymap_reference_file,
             keymap_reference_translation_file],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def process_keymap_reference_card(file_path, result_file=None):
        """
        处理快捷键参考文件
        来自：https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf
        保存后将其复制出来，然后用“【”划分快捷键，再进行一次处理
        :param file_path:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file_path, '_modified', 'properties')
        lines = filex.read_lines(file_path)
        if lines is None:
            return
        result = []
        # 以一个或多个#开头，接内容
        p_title = re.compile(r'^(#+)\s?(.*)')
        for line in lines:
            line = line.replace('\n', '')
            line = re.sub(p_title, r'[\1] \2', line)
            if '【' in line:
                split_result = line.split('【')
                line = '* %s' % split_result[0]
            result.append(line + '\n')
        filex.write_lines(result_file, result)

    @staticmethod
    def process_keymap_reference_card_translation(en_file, cn_file, result_file=None):
        """
        将翻译结果转为md文件
        :param en_file:
        :param cn_file:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(en_file, '_result', 'md')
        en_lines = filex.read_lines(en_file)
        cn_lines = filex.read_lines(cn_file)
        if en_lines is None or cn_lines is None:
            return None

        # 以[]中一个或多个#开头，接内容
        p_title = re.compile(r'^\[(#+)\]\s?(.*)')
        result = []
        for i in range(len(cn_lines)):
            line = cn_lines[i]
            line = encodex.unicode_str_to_chinese(line)
            line = re.sub(p_title, r'\1 \2', line)
            en_line = en_lines[i].replace('\n', '')
            if '【' in en_line:
                shortcut = en_line.split('【')[1]
                line = line.replace('* ', "")
                line = '* %-30s%s' % ('【%s】' % shortcut, line)
            result.append(line)
        filex.write_lines(result_file, result)


if __name__ == '__main__':
    KeymapReference().main()
