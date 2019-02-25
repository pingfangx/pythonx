import re
from xml.etree import ElementTree as Et

from tool.android.android_studio_translator import ActionsBundle
from tool.android.android_studio_translator.tools import Tools
from xx import filex
from xx import iox


class KeymapDefault:
    """
    AndroidStudio的默认快捷键文件
    [AndroidStudio翻译(4)-所有默认快捷键整理及翻译](http://blog.pingfangx.com/2356.html)
    """

    def main(self):
        file_pre = '../actions_bundle/'
        en_add_file = file_pre + ActionsBundle.en_add_file
        en_add_modified_translation_file = ActionsBundle.en_add_modified_translation_file

        keymap_default_file = 'data/keymap_default.xml'
        action_list = [
            ['退出', exit],
            ['处理默认快捷键', self.process_default_keymap, keymap_default_file, en_add_file,
             en_add_modified_translation_file],
            ['读取所有文件中的快捷键', self.get_shortcut_from_dir,
             r'C:\Users\Administrator\Desktop\翻译整理\包\original\keymaps']
        ]
        iox.choose_action(action_list)

    @staticmethod
    def process_default_keymap(keymap_file, en_file, cn_file, sort=True, result_file=None):
        """
        解析AndroidStudio的快捷键配置文件为文本
        :param keymap_file: 快捷键文件，位于/lib/resources.jar，之前的版本为idea/Keymap_Default.xml，pre版改为keymaps/$data.xml
        :param en_file: 英文文件,ActionsBundle.properties
        :param cn_file: 英文文件的翻译
        :param sort: 是否需要按快捷键翻译
        :param result_file:
        :return:
        """
        if result_file is None:
            if sort:
                result_file = filex.get_result_file_name(keymap_file, '_parsed_sorted', 'md')
            else:
                result_file = filex.get_result_file_name(keymap_file, '_parsed', 'md')
        keymap_dict = KeymapDefault.get_keymap_dict_from_file(keymap_file)
        if keymap_dict is None:
            return
        cn_cn_file = filex.get_result_file_name(cn_file, '_cn_result')
        Tools.change_unicode_to_chinese(cn_file, cn_cn_file)
        en_dict = Tools.get_dict_from_file(en_file)
        cn_dict = Tools.get_dict_from_file(cn_cn_file)
        result_list = []
        # 因为可能有重复的，所以手动构建再排序
        shortcut_id_list = []
        for action_id, shortcut in keymap_dict.items():
            shortcut_id_list.append('%s---%s' % (shortcut, action_id))
        if sort:
            shortcut_id_list = sorted(shortcut_id_list, key=KeymapDefault.sort_shortcut)
        for shortcut_id in shortcut_id_list:
            shortcut, action_id = shortcut_id.split('---')
            action_name = 'action.%s.text' % action_id
            if action_name in en_dict.keys():
                # print('有key %s' % action_name)
                en_value = en_dict[action_name]
                if action_name in cn_dict.keys():
                    cn_value = cn_dict[action_name]
                else:
                    cn_value = '【未翻译】'
            else:
                en_value = action_id
                cn_value = '【未记录未翻译】'
            result_list.append('* 【%s】%s(%s)\n' % (shortcut, cn_value, en_value))
        filex.write_lines(result_file, result_list)

    @staticmethod
    def sort_shortcut(shortcut):
        """
        排序快捷方式
        :param shortcut:
        :return:
        """
        # 因为用了.*所以，前后都不能为数字，否则可能会将数字匹配到前面或后面一部分
        result = re.sub(r'(?<!\d)(\d)(?!\d)', r'0\1', shortcut)
        if shortcut != result:
            # print('%s替换为%s' % (shortcut, result))
            shortcut = result
        return shortcut

    @staticmethod
    def get_keymap_dict_from_file(keymap_file, translate_key=True):
        """
        获取快捷键字典
        :param keymap_file:
        :param translate_key: 是否翻译key
        :return:
        """
        replace_list = [
            ['Add', 'Numpad +'],
            ['Subtract', 'Numpad -'],
            ['Multiply', 'Numpad *'],
            ['Divide', 'Numpad /'],
            ['Equals', '='],

            ['Left', '向左箭头'],
            ['Right', '向右箭头'],
            ['Up', '向上箭头'],
            ['Down', '向下箭头'],

            ['Page_up', 'Page Up'],
            ['Page_down', 'Page Down'],
            ['Back_space', 'Backspace'],
            ['Open_bracket', '['],
            ['Close_bracket', ']'],
            ['Back_quote', '后引号'],
            ['Quote', '引号'],
            ['Context_menu', '上下文菜单'],
            ['Space', '空格'],

            ['Button1', '左键'],
            ['Button2', '右键'],

            ['Control', 'Ctrl'],
            ['Escape', 'Esc'],

            ['Period', '句点'],
            ['Slash', '/'],
        ]
        try:
            tree = Et.parse(keymap_file)
        except Et.ParseError:
            print('解析文件失败' + keymap_file)
            return None
        keymap = tree.getroot()
        keymap_dict = dict()
        for action in keymap.iter('action'):
            if 'id' not in action.attrib.keys():
                continue
            action_id = action.attrib['id']
            if 'use-shortcut-of' in action.attrib.keys():
                # 标明了使用快捷键
                keymap_dict[action_id] = 'same with ' + action.attrib['use-shortcut-of']
                continue
            shortcut_key_list = []
            # 快捷键分为键盘和鼠标，而且可能有多个，所以不查找，直接遍历
            for shortcut in action:
                tag = shortcut.tag
                if 'shortcut' not in tag:
                    # 只处理快捷键
                    continue
                if 'keymap' in shortcut.attrib.keys():
                    keymap_type = shortcut.attrib['keymap']
                    if keymap_type != '$default':
                        # 如果不是默认类型的快捷键不处理
                        continue
                # 每个快捷键可能有第一键、第二键，所以对属性直接拼接
                shortcut_key = []
                for key, value in shortcut.attrib.items():
                    if 'keymap' in key:
                        # 不处理快捷键这个
                        continue
                    keys = []
                    for key in value.split(' '):
                        key = key.capitalize()
                        if translate_key:
                            for replace in replace_list:
                                # 不使用replace，直接完整比较
                                if key == replace[0]:
                                    key = replace[1]
                        keys.append(key)
                    shortcut_key.append('+'.join(keys))
                shortcut_key_list.append(','.join(shortcut_key))
            # 可能有多组快捷键
            shortcut_key_str = ';'.join(shortcut_key_list)
            if shortcut_key_str != '':
                keymap_dict[action_id] = shortcut_key_str
        return keymap_dict

    @staticmethod
    def get_shortcut_from_dir(dir_path):
        """
        从目录中读取所有文件中的快捷键
        :param dir_path:
        :return:
        """
        file_list = filex.list_file(dir_path, r'\.xml$')
        for file in file_list:
            keymap_dict = KeymapDefault.get_keymap_dict_from_file(file)
            if keymap_dict:
                print('\n处理' + file)
                print(keymap_dict)


if __name__ == '__main__':
    KeymapDefault().main()
