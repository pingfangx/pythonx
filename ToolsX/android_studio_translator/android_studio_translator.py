import re
from xml.etree import ElementTree as Et

from xx import encodex
from xx import filex
from xx import iox


class AndroidStudioTranslator:
    def main(self):
        # 1原文件
        en_file = 'data/ActionsBundle_en.properties'
        # 2汉化文件
        unicode_file = 'data/ActionsBundle_unicode.properties'
        # 3转为中文
        cn_file = 'data/ActionsBundle_cn.properties'
        # 4修改断句的文件
        cn_modified_file = 'data/ActionsBundle_cn_modified.properties'
        # 5处理快捷方式的文件
        cn_modified_shortcut_file = 'data/ActionsBundle_cn_modified_shortcut.properties'
        # 6手动完成的keymap文件
        keymap_file = 'data/keymap.txt'

        # 默认快捷键的
        # 删除快捷键，删除省略号，补充没有的操作
        en_file_modified = 'keymap/default/ActionsBundle_en_modified.properties'
        keymap_default_file = 'keymap/default/keymap_default.xml'
        cn_file_modified = 'keymap/default/ActionsBundle_en_modified_zh_CN_cn_result.properties'
        action_list = [
            ['退出', exit],
            ['参照翻译(未翻译保留)', self.translate_file_by_reference, en_file, cn_modified_file],
            ['参照翻译(未翻译标记)', self.translate_file_by_reference, en_file, cn_modified_file, None, '%s=%s【未翻译】'],
            ['将文件的unicode转为中文', self.change_unicode_to_chinese,
             'keymap/default/ActionsBundle_en_modified_zh_CN.properties'],
            ['将文件的中文转为unicode', self.change_chinese_to_unicode, cn_file],
            ['处理快捷方式（未翻译留空）', self.handle_shortcut, en_file, cn_modified_file, cn_modified_shortcut_file],
            ['将中文翻译结果导出为OmegaT数据', self.convert_to_omegat_dict, en_file, cn_modified_shortcut_file,
             'data/project_save.tmx.xml'],
            ['处理keymap文件', self.handle_keymap_file, en_file, keymap_file],
            ['处理翻译完的keymap文件', self.handle_translated_keymap_file,
             r"E:\workspace\TranslatorX\AndroidStudio\source\keymap_with_desc_delete_ellipsis.properties",
             r"E:\workspace\TranslatorX\AndroidStudio\target\keymap_with_desc_delete_ellipsis_zh_CN.properties"],
            ['删除文件中的快捷方式', self.delete_shortcut, en_file],
            ['删除OmegaT翻译记忆文件中的快捷方式', self.delete_shortcut_of_omegat, 'data/project_save2.tmx'],
            ['删除文件中的省略号', self.delete_ellipsis, 'data/result/keymap_with_desc.properties'],
            ['删除OmegaT翻译记忆文件中的省略号', self.delete_ellipsis_of_omegat, 'data/project_save2.tmx'],
            ['处理默认快捷键', self.process_default_keymap, keymap_default_file, en_file_modified, cn_file_modified],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def change_unicode_to_chinese(file_path, output_file=None):
        """
        将unicode转为中文
        :param file_path:源文件 
        :param output_file: 输出文件
        :return: 
        """
        if output_file is None:
            output_file = filex.get_result_file_name(file_path, '_cn_result')

        lines = filex.read_lines(file_path)
        if lines is None:
            return

        result = []
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                line = '%s=%s' % (key_value[0], encodex.unicode_str_to_chinese(key_value[1]))
            result.append(line + '\n')
        filex.write_lines(output_file, result)

    @staticmethod
    def change_chinese_to_unicode(file_path, output_file=None):
        """
        将中文转为unicode
        :param file_path: 
        :param output_file: 
        :return: 
        """
        if output_file is None:
            output_file = filex.get_result_file_name(file_path, '_unicode_result')

        lines = filex.read_lines(file_path)
        if lines is None:
            return

        result = []
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                line = '%s=%s' % (key_value[0], encodex.chinese_to_unicode(key_value[1]))
            result.append(line + '\n')
        filex.write_lines(output_file, result)

    def handle_shortcut(self, en_file, cn_file, result_file=None):
        """
        处理快捷键，将_字母替换为(_字母)
        :param en_file: 
        :param cn_file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_shortcut_result')

        en_dict = filex.get_dict_from_file(en_file)
        cn_dict = filex.get_dict_from_file(cn_file)
        count = 0
        for (k, v) in en_dict.items():
            if '_' in v:
                index = v.find('_')
                shortcut = v[index + 1:index + 2]
                # 包含快捷键
                if k in cn_dict.keys():
                    # 都有
                    cn_value = cn_dict[k]
                    count += 1
                    # 已经是(_字母结)结尾的，重新替换一遍
                    p = re.compile(r'(.*)(\(_\w\))')
                    if re.match(p, cn_value) is not None:
                        replace_result = re.sub(p, r'\1' + '(_%s)' % shortcut, cn_value)
                        print('替换%d,key=%s,v=%s,cn=%s,r=%s' % (count, shortcut, v, cn_value, replace_result))
                    else:
                        replace_result = cn_value.replace('_', '') + '(_%s)' % shortcut
                        print('添加%d,key=%s,v=%s,cn=%s,r=%s' % (count, shortcut, v, cn_value, replace_result))
                    cn_dict[k] = replace_result
        result = self.translate_file_by_dict(en_file, cn_dict, '')  # 重新翻译
        filex.write_lines(result_file, result)

    def translate_file_by_reference(self, en_file, cn_file, result_file=None, untranslated_replace=None):
        """
        根据参考翻译文件
        :param en_file:英文 
        :param cn_file: 参考中文
        :param result_file: 结果文件
        :param untranslated_replace:未翻译时替换 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(en_file, '_translation_result')

        translation_dict = filex.get_dict_from_file(cn_file)
        result = self.translate_file_by_dict(en_file, translation_dict, untranslated_replace)

        filex.write_lines(result_file, result)

    @staticmethod
    def translate_file_by_dict(file_path, translation_dict, untranslated_replace=None):
        """
        翻译文件
        :param file_path: 要翻译的文件
        :param translation_dict: 字典
        :param untranslated_replace: 未翻译的用什么替换，（将会执行untranslated % (key_value[0], key_value[1])），
        如果执行失败则直接用其值替换
        默认为None，如果为None表示不替换
        :return: 
        """
        lines = filex.read_lines(file_path)
        if lines is None:
            return None

        result = []
        untranslated_count = 0
        for line in lines:
            line = line.replace('\n', '')
            if '=' in line:
                key_value = line.split('=', 1)
                # 翻译
                key = key_value[0]
                if key in translation_dict.keys():
                    translation = translation_dict[key]
                    if translation is not None and translation != '':
                        line = '%s=%s' % (key_value[0], translation)
                else:
                    # line += '待翻译'
                    untranslated_count += 1
                    print('%d-%s-未翻译' % (untranslated_count, line))
                    if untranslated_replace is not None:
                        try:
                            line = untranslated_replace % (key_value[0], key_value[1])
                        except TypeError:
                            line = untranslated_replace
            result.append(line + '\n')
        return result

    def convert_to_omegat_dict(self, en_file, cn_file, output_file=None):
        """
        将翻译结果转为omegaT的字典
        :param en_file: 英文文件
        :param cn_file: 中文文件
        :param output_file: 输出文件
        :return: 
        """
        if output_file is None:
            output_file = filex.get_result_file_name(cn_file, '_omegat_result', 'xml')

        en_dict = filex.get_dict_from_file(en_file)
        cn_dict = filex.get_dict_from_file(cn_file)

        tmx = Et.Element('tmx')
        tmx.attrib['version'] = '1.1'
        Et.SubElement(tmx, 'header')
        body = Et.SubElement(tmx, 'body')
        for (k, v) in cn_dict.items():
            if k in en_dict.keys():
                en_value = en_dict[k]
                cn_value = v
                # 判断是否有多个句子，"."加一个空格
                added = False
                if '. ' in en_value:
                    en_split = en_value.split('. ')
                    if en_split[1] != '':
                        # 包含“.”，不是在最后的“...”
                        # 检查中文
                        if '。 ' in cn_value:
                            cn_split = cn_value.split('。 ')
                            if len(en_split) == len(cn_split):
                                added = True
                                # 中英长度相等
                                for i in range(len(en_split)):
                                    self.add_translate_element(body, en_split[i], cn_split[i])
                                    print('分开添加:' + cn_split[i])
                            else:
                                print('')
                                print(en_value)
                                print(cn_value)
                                print('%d,%d' % (len(en_split), len(cn_split)))
                        else:
                            print('')
                            print(en_value)
                            print(cn_value)
                            print('不包含')
                if not added:
                    self.add_translate_element(body, en_value, cn_value)

        tree = Et.ElementTree(tmx)
        tree.write(output_file, encoding='utf-8')
        print('输出为' + output_file)

    @staticmethod
    def add_translate_element(element, en, cn):
        """
        向element中添加一个翻译
        :param element: 
        :param en
        :param cn
        :return: 
        """

        tu = Et.SubElement(element, 'tu')
        # 英文
        tuv = Et.SubElement(tu, 'tuv')
        tuv.attrib['lang'] = 'EN-US'
        seg = Et.SubElement(tuv, 'seg')
        seg.text = en
        # 中文
        tuv2 = Et.SubElement(tu, 'tuv')
        tuv2.attrib['lang'] = 'ZH-CN'
        seg2 = Et.SubElement(tuv2, 'seg')
        seg2.text = cn

    @staticmethod
    def handle_keymap_file(en_file, cn_file, result_file=None):
        """
        将一行一行的keymap重新处理
        导出为.properties，这样OmegaT处理时会换照配置文件去处理
        我们以[#]或[desc]加空格为开头，会被过滤器正确解析
        :param en_file: 
        :param cn_file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_with_desc', 'properties')

        lines = filex.read_lines(cn_file)
        if lines is None:
            return

        en_dict = filex.get_dict_from_file(en_file)
        # 反转
        reversed_dict = {value: key for key, value in en_dict.items()}

        count = 0
        desc_count = 0
        result = []
        for line in lines:
            line = line.replace('\n', '')
            if line.startswith('#'):
                old_line = line
                # 因为有加了#，所以处理下
                line = line.lstrip('# ')
                # 相差的长度是trip掉的，注意在替换了\n之后
                prefix = old_line[0:len(old_line) - len(line)].rstrip()
            else:
                prefix = '#' * 5
            append = ''
            if line in reversed_dict.keys():
                count += 1
                key = reversed_dict[line]
                if key.endswith('.text'):
                    desc_key = key[:-len('.text')] + '.description'
                    if desc_key in en_dict.keys():
                        desc = en_dict[desc_key]
                        desc_count += 1
                        print('%d/%d,%s,key=%s,desc=%s' % (count, desc_count, line, key, desc))
                        # 有描述，添加
                        append = '\n\n%s %s' % ('[desc]', desc)
            line = '\n\n[%s] %s%s' % (prefix, line, append)
            result.append(line)
        filex.write_lines(result_file, result)

    @staticmethod
    def handle_translated_keymap_file(en_file, cn_file, result_file=None):
        """
        处理翻译完的文件
        :param en_file: 
        :param cn_file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_final')
        en_lines = filex.read_lines(en_file)
        cn_lines = filex.read_lines(cn_file)
        if cn_lines is None:
            return

        result = []
        p_title = re.compile(r'^\[(#+)\]\s?(.*)')
        p_title2 = re.compile(r'(\n*)(#*\s)(.*)')
        p_desc = re.compile(r'^\[desc\]\s?(.*)')
        p_comment = re.compile(r'^#\[(x+)\](.*)')
        for i in range(len(cn_lines)):
            line = cn_lines[i].replace('\n', '')
            if line.startswith('#'):
                # 以#开头不翻译，取原文
                line = en_lines[i].replace('\n', '')
                match = re.match(p_comment, line)
                if match is not None:
                    # 注释
                    start_number = match.group(1)
                    if len(start_number) == 1:
                        # 1颗星标记基本注释
                        replace_result = '  \n译注：%s' % (match.group(2))
                    else:
                        # 2星以上为加重注释
                        last_line = result[-1]
                        if '★' not in last_line:
                            last_line_match = re.match(p_title2, last_line)
                            if last_line_match is not None:
                                start_replace = '★' * (len(start_number) - 1)
                                last_line = re.sub(p_title2, r'\1\2*%s\3%s*' % (start_replace, start_replace),
                                                   last_line)
                                print('替换【%s】为【%s】' % (result[-1], last_line))
                                result[-1] = last_line
                        replace_result = '  \n译注：%s' % (match.group(2))
                    # print('替换【%s】为【%s】' % (line, replace_result))
                    line = '%s' % replace_result
            else:
                # 不以#开头
                line = encodex.unicode_str_to_chinese(line)
                en_line = en_lines[i].replace('\n', '')
                match = re.match(p_title, line)
                if match is not None:
                    # 是标题
                    en_match = re.match(p_title, en_line)
                    if len(en_match.group(1)) == 5:
                        replace_result = '\n\n%s（%s）' % (en_match.group(2), match.group(2))
                    else:
                        replace_result = '\n\n%s %s（%s）' % (en_match.group(1), en_match.group(2), match.group(2))
                    # print('\n替换【%s】为【%s】' % (line, replace_result))
                    line = '%s' % replace_result
                else:
                    desc_cn_match = re.match(p_desc, line)
                    if desc_cn_match is not None:
                        # 是描述
                        desc_en_match = re.match(p_desc, en_line)
                        replace_result = '  \n%s  \n描述：%s' % (desc_en_match.group(1), desc_cn_match.group(1))
                        # print('\n描述替换【%s】为【%s】' % (line, replace_result))
                        line = '%s' % replace_result

            result.append(line)
        filex.write_lines(result_file, result)

    @staticmethod
    def delete_shortcut(file, result_file=None):
        """
        删除文件中的快捷方式
        :param file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file, '_delete_shortcut')
        lines = filex.read_lines(file)
        if lines is None:
            return
        # (.*懒惰)(空白?点一次或多次)
        p = re.compile(r'(.*?)(\s?\(_\w\))')
        result = []
        for line in lines:
            line = line.replace('\n', '')
            if line is None:
                continue
            if '_' in line:
                if re.match(p, line) is not None:
                    replace_result = re.sub(p, r'\1', line)
                    print('删除【%s】为【%s】' % (line, replace_result))
                else:
                    replace_result = line.replace('_', '')
                    print('替换【%s】为【%s】' % (line, replace_result))
                line = replace_result
            result.append(line + '\n')

        filex.write_lines(result_file, result)
        print('输出为' + result_file)

    @staticmethod
    def delete_shortcut_of_omegat(file, result_file=None):
        """
        删除文件中的快捷方式，本来应该在导出的时候就删除，但是已经改了一些了，只好处理
        :param file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file, '_delete_shortcut')
        tree = Et.parse(file)
        tmx = tree.getroot()
        body = tmx.find('body')
        # (.*懒惰)(空白?\(下划线字母\))
        p = re.compile(r'(.*?)(\s?\(_\w\))')
        for seg in body.iter('seg'):
            content = seg.text
            if content is None:
                continue
            if '_' in content:
                if re.match(p, content) is not None:
                    replace_result = re.sub(p, r'\1', content)
                    print('删除【%s】为【%s】' % (content, replace_result))
                else:
                    replace_result = content.replace('_', '')
                    print('替换【%s】为【%s】' % (content, replace_result))
                seg.text = replace_result

        tree.write(result_file, encoding='utf-8')
        print('输出为' + result_file)

    @staticmethod
    def delete_ellipsis(file, result_file=None):
        """
        删除每一行结尾的“.”，包括一个（句号）或多个（如省略号）
        :param file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file, '_delete_ellipsis')
        lines = filex.read_lines(file)
        if lines is None:
            return
        # (.*懒惰)(空白?点一次或多次)
        p = re.compile(r'(.*?)(\s?\.+)$')
        result = []
        for line in lines:
            line = line.replace('\n', '')
            if line is None:
                continue
            if '.' in line:
                if re.match(p, line) is not None:
                    replace_result = re.sub(p, r'\1', line)
                    print('删除【%s】为【%s】' % (line, replace_result))
                    line = replace_result
                else:
                    print('未处理【%s】' % line)
            result.append(line + '\n')

        filex.write_lines(result_file, result)
        print('输出为' + result_file)

    @staticmethod
    def delete_ellipsis_of_omegat(file, result_file=None):
        """
        删除每一行结尾的“.”，包括一个（句号）或多个（如省略号）
        :param file: 
        :param result_file: 
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file, '_delete_ellipsis')
        tree = Et.parse(file)
        tmx = tree.getroot()
        body = tmx.find('body')
        # (.*懒惰)(空白?点一次或多次)
        p = re.compile(r'(.*?)(\s?\.+)$')
        for seg in body.iter('seg'):
            content = seg.text
            if content is None:
                continue
            if '.' in content:
                if re.match(p, content) is not None:
                    replace_result = re.sub(p, r'\1', content)
                    print('删除【%s】为【%s】' % (content, replace_result))
                else:
                    replace_result = content
                    print('未处理【%s】为【%s】' % (content, replace_result))
                seg.text = replace_result

        tree.write(result_file, encoding='utf-8')
        print('输出为' + result_file)

    @staticmethod
    def sort_shortcut(shortcut):
        """
        排序快捷方式
        :param shortcut: 
        :return: 
        """
        # 因为用了.*所以，前后都不能为数字，否则可能会将数字匹配到前面或后面一部分
        p = re.compile('(.*?\D)(\d)(\D.*)')
        match = p.match(shortcut)
        if match is not None:
            result = '%s0%s%s' % (match.group(1), match.group(2), match.group(3))
            print('%s替换为%s' % (shortcut, result))
        else:
            result = shortcut
        return result

    def process_default_keymap(self, keymap_file, en_file, cn_file, sort=True, result_file=None):
        """
        解析AndroidStudio的快捷键配置文件为文本
        :param keymap_file: 快捷键文件，位于/lib/resources.jar，之前的版本为idea/Keymap_Default.xml，pre版改为keymaps/$default.xml
        :param en_file: 英文文件,ActionsBundle.properties
        :param cn_file: 英文文件的翻译
        :param sort: 是否需要按快捷键翻译
        :param result_file: 
        :return: 
        """
        if result_file is None:
            if sort:
                result_file = filex.get_result_file_name(keymap_file, '_parsed_sorted')
            else:
                result_file = filex.get_result_file_name(keymap_file, '_parsed')
        keymap_dict = self.get_default_keymap(keymap_file)
        if keymap_dict is None:
            return
        en_dict = filex.get_dict_from_file(en_file)
        cn_dict = filex.get_dict_from_file(cn_file)
        result_list = []
        # 因为可能有重复的，所以手动构建再排序
        shortcut_id_list = []
        for action_id, shortcut in keymap_dict.items():
            shortcut_id_list.append('%s---%s' % (shortcut, action_id))
        if sort:
            shortcut_id_list = sorted(shortcut_id_list, key=self.sort_shortcut)
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
    def get_default_keymap(keymap_file):
        """
        获取快捷键字典
        :param keymap_file: 
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
        tree = Et.parse(keymap_file)
        keymap = tree.getroot()
        keymap_dict = dict()
        for action in keymap.iter('action'):
            id = action.attrib['id']
            shortcut_key_list = []
            # 快捷键分为键盘和鼠标，而且可能有多个，所以不查找，直接遍历
            for shortcut in action:
                # shortcut_type = shortcut.tag
                # 每个快捷键可能有第一键、第二键，所以对属性直接拼接
                shortcut_key = []
                for value in shortcut.attrib.values():
                    keys = []
                    for key in value.split(' '):
                        key = key.capitalize()
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
                keymap_dict[id] = shortcut_key_str
        return keymap_dict


if __name__ == '__main__':
    AndroidStudioTranslator().main()
