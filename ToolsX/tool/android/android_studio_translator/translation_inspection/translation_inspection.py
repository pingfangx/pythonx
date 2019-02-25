# coding=utf-8
import re

from tool.android.android_studio_translator.delete_action import DeleteAction
from tool.android.android_studio_translator.tools import Tools
from xx import filex
from xx import iox


class TranslationInspection:
    """
    有一个问题，就是判断''被错误翻译成""的时候，没有判断引号中的内容是否一致
    """

    @staticmethod
    def get_inspection_list():
        return [
            StandardTranslation.inspect_translation,
            TranslationInspection.inspect_double_quote,
            TranslationInspection.inspect_single_quote,
            TranslationInspection.inspect_double_single_quote,
            TranslationInspection.inspect_parentheses,
            TranslationInspection.inspect_ends_symbol,
            TranslationInspection.inspect_tag,
            TranslationInspection.inspect_short_cut,
            TranslationInspection.inspect_underline_short_cut,
            TranslationInspection.inspect_space,
            TranslationInspection.inspect_space_2,
            TranslationInspection.inspect_serial_number,
        ]

    def main(self):
        pseudo_file = 'data/project_save.tmx'
        translation_file = 'data/project_save.tmx'
        inspection_list = TranslationInspection.get_inspection_list()
        action_list = [
            ['退出', exit],
            ['检查', self.inspect_file, translation_file, translation_file, inspection_list, None, False, True],
            ['测试', self.test],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def test():
        en = 'Redundant directive \'\'requires {0}\'\''
        cn = '多余的指令 \'\' requires {0}\'\''
        inspection_list = TranslationInspection.get_inspection_list()
        for inspection in inspection_list:
            old = cn
            cn = inspection(en, cn, True)
            print(u'\nafter %s\n%s\n%s\n%s' % (inspection.__name__, en, old, cn))

    @staticmethod
    def inspect_file(pseudo_file, translation_file, inspection_list, result_file=None, print_msg=False,
                     print_change=False):
        """

        :param pseudo_file: 伪翻译文件，也可以与翻译文件相同，用于自校检
        :param translation_file: 翻译文件
        :param inspection_list: 要检测的方法列表，如检测tips时是不需要检测快捷方式的
        :param result_file: 结果文件
        :param print_msg: 是否输出操作时的消息
        :param print_change: 是否输出更改时的消息，如果2个都置为False，可以查看需要处理的内容
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(translation_file, '_inspection')
        pseudo_dict = Tools.get_dict_from_omegat(pseudo_file)
        translation_dict = Tools.get_dict_from_omegat(translation_file)
        print(u'pseudo size is %d' % (len(pseudo_dict)))
        print(u'translation size is %d' % (len(translation_dict)))
        result = dict()
        i = 0
        for en in pseudo_dict.keys():
            cn_key = None
            if en in translation_dict.keys():
                cn_key = en
            else:
                abbreviated_en = DeleteAction.delete_all_symbol_of_string(en, False)
                if abbreviated_en in translation_dict.keys():
                    cn_key = abbreviated_en
            if cn_key:
                value = translation_dict[cn_key]
                if not value:
                    continue
                translation_dict.pop(cn_key)
                old = value
                for inspection in inspection_list:
                    value = inspection(en, value, print_msg)
                if old != value:
                    if print_change:
                        i += 1
                        print(u'\n%d.\n【%s】根据【%s】被修改为\n【%s】\n' % (i, old, en, value))
                result[en] = value
            else:
                print(u'不包含key:%s' % en)
        print(u'remain translation size %d' % (len(translation_dict)))
        Tools.save_omegat_dict(result, result_file)

    @staticmethod
    def inspect(en, cn):
        """提取出方法方便外部调用"""
        inspection_list = TranslationInspection.get_inspection_list()
        for inspection in inspection_list:
            cn = inspection(en, cn, False)
        return cn

    @staticmethod
    def inspect_tag(en, cn, print_msg=False):
        """检查标签"""
        pattern = r'</?.+?>'
        en_all_match = re.findall(pattern, en)
        cn_all_match = re.findall(pattern, cn)
        # 删除空格
        for i in range(len(cn_all_match)):
            cn_match = cn_all_match[i]
            if ' ' in cn_match:
                # 包含空格
                cn_match_without_space = cn_match.replace(' ', '').lower()
                if cn_match_without_space in en_all_match:
                    # 两处都要替换
                    cn = cn.replace(cn_match, cn_match_without_space)
                    cn_all_match[i] = cn_match_without_space
        if not TranslationInspection.compare_list(en_all_match, cn_all_match):
            print(u'en=【%s】\ncn=【%s】' % (en, cn))
            print(en_all_match)
            print(cn_all_match)
            print(u'')

        # 保留标签
        need_same_tag = True
        if need_same_tag:
            pattern = r'<(\w\d+)>(.+?)</\1>'
            en_all_match = re.findall(pattern, en)
            cn_all_match = re.findall(pattern, cn)
            if en_all_match and cn_all_match:
                for tag, content in en_all_match:
                    for cn_tag, cn_content in cn_all_match:
                        if tag == cn_tag:
                            # 标签相等，替换内容
                            cn = cn.replace('<%s>%s</%s>' % (cn_tag, cn_content, cn_tag),
                                            '<%s>%s</%s>' % (tag, content, tag))
        return cn

    @staticmethod
    def compare_list(list1, list2):
        """比较两个数组，忽略元素的顺序"""
        if list1 is None and list2 is None:
            # 都为 None
            return True
        elif list1 is None or list2 is None:
            # 有一个为 None
            print(u'有一个 list 为 None')
            return False

        # 忽略换行
        tag = '<br>'
        while tag in list1:
            list1.remove(tag)
        while tag in list2:
            list2.remove(tag)
        if len(list1) != len(list2):
            print(u'标签长度不相等')
            return False

        chinese_pattern = re.compile(u'([\u4e00-\u9fa5])')
        for i in list2:
            if re.search(chinese_pattern, i):
                # 忽略中文
                continue
            if i not in list1 or list1.count(i) != list2.count(i):
                print(u'元素不存在或数量不等', i)
                return False
        return True

    @staticmethod
    def inspect_serial_number(en, cn, print_msg=False):
        """检查序号是否还有"""
        pattern = r'{\d}'
        # 可用来检查
        # pattern = r'{.+?}'
        # pattern = r'({\d(, choice.+)?})'
        en_all_match = re.findall(pattern, en)
        if en_all_match:
            cn_all_match = re.findall(pattern, cn)
            if not cn_all_match:
                print(u'\n中文中没有序号\nen=【%s】\ncn=【%s】' % (en, cn))
            elif len(en_all_match) != len(cn_all_match):
                print(u'\n中英文序号数量不一致\nen=【%s】\ncn=【%s】' % (en, cn))
        return cn

    @staticmethod
    def inspect_space(en, cn, print_msg=False):
        """
        检查汉字与英文（或{\d}）之间是否添加了空格
        """
        chinese_pattern = u'([\u4e00-\u9fa5])'
        # 字母，或{0}，或''{0}''
        # need_space_pattern = r'([a-zA-Z]|{\d}+|\'\'{\d}\'\')'

        # 测试发现有一些没有完全替换，使用 .+? 也不会过多替换
        # need_space_pattern = r'([a-zA-Z]|{\d}+|\'\'.+?\'\')'

        # 再进一步，即使单个引号也不会有错误的
        # need_space_pattern = r'([a-zA-Z]|{\d}+|\'.+?\')'
        # 补充双引号
        need_space_pattern = r'([a-zA-Z]|\d|{\d}+|\'.+?\'|\".+?\")'
        double_quote_pattern = r'\''

        cn = re.sub(chinese_pattern + need_space_pattern, r'\1 \2', cn)
        cn = re.sub(need_space_pattern + chinese_pattern, r'\1 \2', cn)

        # 中文跟标签,标签中为不是中文
        # 由于使用了 u'' ，所以后面的 \\2 要义
        need_space_pattern3 = u'([\u4e00-\u9fa5])<(.+?)>([^\u4e00-\u9fa5]+?)</\\2>'
        cn = re.sub(need_space_pattern3, r'\1 <\2>\3</\2>', cn)
        need_space_pattern4 = u'<(.+?)>([^\u4e00-\u9fa5]+?)</\\1>([\u4e00-\u9fa5])'
        cn = re.sub(need_space_pattern4, r'<\1>\2</\1> \3', cn)

        all_match = re.findall(r'\'\s(.+?)\s\'', cn)
        if all_match:
            for match in all_match:
                match_without_quote_space = '\' %s \'' % match
                match_without_quote = '\'%s\'' % match
                if match_without_quote in en:
                    if print_msg:
                        print(u'翻译的双引号中有空格，而原文没有，将其空格删除【%s】' % match_without_quote_space)
                    cn = cn.replace(match_without_quote_space, match_without_quote)

        if print_msg:
            if re.search(chinese_pattern + double_quote_pattern, cn):
                print(u'【%s】在中文后有相连的引号' % cn)
            if re.search(double_quote_pattern + chinese_pattern, cn):
                print(u'【%s】在中文前有相连的引号' % cn)
        # 特殊的不替换
        cn = cn.replace('平方 X', '平方X')
        return cn

    @staticmethod
    def inspect_space_2(en, cn, print_msg=False):
        """
        该方法检查 序号与引号之前是否加上空格
        {0} ''{1}''
        :param en:
        :param cn:
        :param print_msg:
        :return:
        """
        # 空格* {0} 空格* '多个 {0} '多个 空格*
        pattern = r"\s*{\d}\s*['\"]+{\d}['\"]+\s*"
        pattern2 = r"\s*['\"]+{\d}['\"]+\s*{\d}\s*"
        match = re.search(pattern, en)
        if match:
            cn_pattern = pattern
        else:
            cn_pattern = pattern2
            match = re.search(pattern2, en)
        if match:
            en_word = match.group()
            if en_word not in cn:
                cn_match = re.search(cn_pattern, cn)
                if not cn_match:
                    print(u'\n%s\n%s\n【%s】不在中文中，并且中文无法匹配正则' % (en, cn, en_word))
                else:
                    # 中文中找到匹配，可以替换
                    cn_word = cn_match.group()
                    replace_word = en_word
                    # 在开头结尾可以去掉空格
                    if cn.startswith(cn_word):
                        # 以其开头
                        replace_word = replace_word.lstrip(' ')
                    else:
                        if en.startswith(en_word):
                            # 英文以其开头，则不会有前导空格，在中文中不以其开头，则应加上空格
                            replace_word = ' ' + replace_word
                    if cn.endswith(cn_word):
                        replace_word = replace_word.rstrip(' ')
                    else:
                        if en.endswith(en_word):
                            # 英文以其结尾，中文不以其结尾，添加末尾空格
                            replace_word += ' '
                    cn = cn.replace(cn_word, replace_word)
        return cn

    @staticmethod
    def inspect_short_cut(en, cn, print_msg=False):
        """
        检查快捷键
        处理&形式快捷方式
        下划线的快捷方式经常会有问题，一定要注意处理
        """
        cn = TranslationInspection.search_and_replace(en, cn, r'(?<!\\)&(\w)', r'(&%s)',
                                                      print_msg=print_msg)
        return cn

    @staticmethod
    def inspect_underline_short_cut(en, cn, print_msg=False):
        """
        检查下划线的快捷方式，这里主要是检查，可能被错误的替换
        """
        if en != cn:
            # 相等不处理
            if '_' in en:
                if en.count('_') == 1:
                    # 只有一个下划线
                    match = re.search(r'_\w', en)
                    if match:
                        append = '(%s)' % match.group()
                        append = append.upper()
                        if cn.endswith(append):
                            if print_msg:
                                print(u'已经以【%s】结尾' % append)
                        elif cn.endswith(append.lower()):
                            if print_msg:
                                print(u'已经以小写的【%s】结尾,替换为大写' % append.lower())
                            cn = cn[: -len(append)]
                            cn += append
                        else:
                            ignore_list = [
                                r'EXIT_CODE',
                                r'directory_path',
                                r'EMPTY_MAP',
                            ]
                            contain_ignore_word = False
                            for ignore_word in ignore_list:
                                if ignore_word in en:
                                    contain_ignore_word = True
                                    break
                            if not contain_ignore_word:
                                print(u'\n可能需要添加快捷方式【%s】' % append)
                                print(u'%s\n%s' % (en, cn))
                    else:
                        if '_' not in cn:
                            print(u'\n%s\n%s' % (en, cn))
                            print(u'没有匹配字母，且不匹配')
                else:
                    if cn.count('_') != en.count('_'):
                        print(u'\n%s\n%s' % (en, cn))
                        print(u'有多个下划线，且数量不匹配')
        shortcut_pattern = '\(_\w\)$'
        match = re.search(shortcut_pattern, cn)
        if match:
            # 有快捷方式
            if '&' in en or en.count('_') == 1:
                pass
            else:
                print(u'\n%s\n%s' % (en, cn))
                print(u'没有 & 或一个下划线，却添加了快捷方式')
        return cn

    @staticmethod
    def search_and_replace(en, cn, pattern, replace, group=1, print_msg=False):
        match = re.search(pattern, en)
        if match is not None:
            content = match.group(group)
            if print_msg:
                print(u'\n【%s】匹配，翻译是【%s】,内容是【%s】' % (en, cn, content))
            append = replace % content
            append = append.upper()
            if cn.endswith(append):
                if print_msg:
                    print(u'已经以【%s】结尾' % append)
            elif cn.endswith(append.lower()):
                if print_msg:
                    print(u'已经以小写的【%s】结尾,替换为大写' % append.lower())
                cn = cn[: -len(append)]
                cn += append
            else:
                ignore_list = [
                    'shortcut:',
                    'productName;',
                    'majorVersion;',
                    'minorVersion;',
                    'majorMinorVersion;',
                    'settingsPath;',
                ]
                contain_ignore = False
                for ignore_word in ignore_list:
                    if '&%s' % ignore_word in cn:
                        contain_ignore = True
                        break
                if not contain_ignore:
                    print(u'【%s】not endswith 【%s】' % (cn, append))
                    cn += append
                else:
                    if print_msg:
                        print(u'忽略')
        return cn

    @staticmethod
    def inspect_ends_symbol(en, cn, print_msg=False):
        """
        检查结尾的符号
        """
        pattern = u'(\s?([.。…\\:：])+)$'
        en_match = re.search(pattern, en)
        if en_match:
            if print_msg:
                print(u'\n【%s】包含结尾符号，翻译是【%s】' % (en, cn))
            en_content = en_match.group(1)
            if en_content == '.':
                # 将句点替换为句号
                en_content = u'。'
            if not re.search(pattern, cn):
                # 忽略已经有的快捷方式
                if not re.search(pattern, re.sub(r'\([_&]\w\)', '', cn)):
                    # 这里要添加的时候把快捷方式删了
                    match = re.search(r'(\([_&]\w\))', cn)
                    if match is not None:
                        cn = re.sub(r'\(([_&]\w\))', '', cn) + en_content + match.group(1)
                    else:
                        cn = cn + en_content
                    if print_msg:
                        print(u'在结尾添加%s' % en_content)
        return cn

    @staticmethod
    def inspect_parentheses(en, cn, print_msg=False):
        """
        检查()不翻译为（），同时如果是方法后的()后面加上空格
        """
        pattern = r'\(.*?\)'
        en_match_list = re.findall(pattern, en)
        if en_match_list:
            if print_msg:
                print(u'\n【%s】包含小括号，翻译是【%s】' % (en, cn))
            if len(en_match_list) == cn.count(u'（') and len(en_match_list) == cn.count(u'）'):
                if print_msg:
                    print(u'被翻译成了【（）】,替换')
                cn = cn.replace(u'（', '(')
                cn = cn.replace(u'）', ')')

            chinese_pattern = u'([\u4e00-\u9fa5])'
            need_space_pattern = r'(\(\))'
            old = cn
            cn = re.sub(need_space_pattern + chinese_pattern, r'\1 \2', cn)
            if old != cn:
                if print_msg:
                    print(u'补充括号后的空格')
        return cn

    @staticmethod
    def inspect_double_single_quote(en, cn, print_msg=False):
        """
        检查''(2个')也按原来的保持''，去除中间的空格，同时前后如果是字母加上空格
        """
        # 因为会有don''t之类的，过滤t
        pattern = r'\'{2}(.+?)\'{2}(?!t)'
        en_match_list = re.findall(pattern, en)
        if en_match_list:
            if print_msg:
                print(u'\n【%s】包含两个单引号，翻译是【%s】' % (en, cn))
            if len(en_match_list) == cn.count(u'“') and len(en_match_list) == cn.count(u'”'):
                if print_msg:
                    print(u'被翻译成了【“”】,替换')
                cn = cn.replace(u'“', '\'\'')
                cn = cn.replace(u'”', '\'\'')
            if len(en_match_list) * 2 == cn.count('"') and '="' not in cn:
                if print_msg:
                    print(u'被翻译成了【"】，替换')
                cn = cn.replace('"', "\'\'")
            old = cn
            # 这里的目的是去掉两个 ' 中间与内容的空格
            # 2个 ' 中间，前后可能有空格，中间 .+（一个或多个），懒惰
            cn = re.sub(r"('+)\s*(.+?)\s*('+)", r"\1\2\3", cn)
            if old != cn:
                if print_msg:
                    print(u'去除单引号前后的空格')
            cn_match_list = re.findall(pattern, cn)
            if not cn_match_list:
                for en_match in en_match_list:
                    all_quote = '\'\'' + en_match + '\'\''
                    if en_match in cn and all_quote not in cn:
                        left_quote = '\'\'' + en_match + '\''
                        right_quote = '\'' + en_match + '\'\''
                        if left_quote in cn:
                            if print_msg:
                                print(u'右边缺\'，添加')
                            cn = cn.replace(left_quote, all_quote)
                        elif right_quote in cn:
                            if print_msg:
                                print(u'左边缺\'，添加')
                            cn = cn.replace(right_quote, all_quote)
                        else:
                            if print_msg:
                                print(u'左右缺\'\'，添加')
                            cn = cn.replace(en_match, all_quote)
            cn_match_list = re.findall(pattern, cn)
            if not cn_match_list:
                print(u'中文中没有结果')
                print(u'\n【%s】包两个单引号，翻译是【%s】,内容是【%s】' % (en, cn, ''))
                return cn
            if len(en_match_list) != len(cn_match_list):
                print(u'匹配结果的大小不相等')
                print(u'\n【%s】包两个单引号，翻译是【%s】,内容是【%s】' % (en, cn, ''))
                return cn
            # 如果前后跟字母，则补充空格
            old = cn
            TranslationInspection.add_space_round_quote(en, cn, pattern, '\'\'', print_msg)
            if old != cn:
                if print_msg:
                    print(u'补充与字母相联的''的空格')
        return cn

    @staticmethod
    def add_space_round_quote(en, cn, pattern, quote, print_msg):
        """添加引号周围的括号"""
        en_match_list = re.findall(pattern, en)
        cn_match_list = re.findall(pattern, cn)
        if len(en_match_list) == len(cn_match_list):
            for i in range(len(en_match_list)):
                en_content = en_match_list[i]
                cn_content = cn_match_list[i]
                if en_content != cn_content and en_content == cn_content.strip():
                    if print_msg:
                        print(u'翻译中引号中的内容带有空格，删除')
                    cn = cn.replace(quote + cn_content + quote, quote + cn_content.strip() + quote)
                    cn_content_with_quotation = cn_content.strip()
                else:
                    cn_content_with_quotation = cn_content
                cn_content_with_quotation = quote + cn_content_with_quotation + quote
                if not cn.startswith(cn_content_with_quotation) and ' ' + cn_content_with_quotation not in cn:
                    cn = cn.replace(cn_content_with_quotation, ' ' + cn_content_with_quotation)
                if not cn.endswith(cn_content_with_quotation) and cn_content_with_quotation + ' ' not in cn:
                    cn = cn.replace(cn_content_with_quotation, cn_content_with_quotation + ' ')
        return cn

    @staticmethod
    def inspect_single_quote(en, cn, print_msg=False):
        """检查单引号"""
        # 只有一个单引号，前后不能有，不知如何表示更好，就写成了这样
        pattern = r'(?<!\')\'(?!\')(.+?)(?<!\')\'(?!\')'
        en_match_list = re.findall(pattern, en)
        if en_match_list:
            if print_msg:
                print(u'\n【%s】包含成对单引号，翻译是【%s】' % (en, cn))

            cn_match_list = re.findall(pattern, cn)
            if len(en_match_list) != len(cn_match_list):
                if len(en_match_list) == cn.count(u'“') and len(en_match_list) == cn.count(u'”'):
                    if print_msg:
                        print(u'被翻译成了【“”】,替换')
                    cn = cn.replace(u'“', '\'')
                    cn = cn.replace(u'”', '\'')
                elif len(en_match_list) == cn.count(u'‘') and len(en_match_list) == cn.count(u'’'):
                    if print_msg:
                        print(u'被翻译成了【‘’】,替换')
                    cn = cn.replace(u'‘', '\'')
                    cn = cn.replace(u'’', '\'')
                elif len(en_match_list) * 2 == cn.count('"'):
                    if print_msg:
                        print(u'被翻译成了【"】,替换')
                    cn = cn.replace('"', '\'')

            cn_match_list = re.findall(pattern, cn)
            if len(en_match_list) != len(cn_match_list):
                ignore_list = [
                    'idea\'s',
                    'Drag\'n\'Drop',
                    'won\'t',
                    'it\'s'
                ]
                contain_ignore_word = False
                for ignore_word in ignore_list:
                    if ignore_word in en:
                        contain_ignore_word = True
                        break
                if not contain_ignore_word:
                    print(u'\n【%s】包含成对单引号，翻译是【%s】' % (en, cn))
                    print(u'匹配结果的大小不相等')
                    print(en_match_list)
                    print(cn_match_list)
                return cn
            for i in range(len(en_match_list)):
                en_content = en_match_list[i]
                cn_content = cn_match_list[i]
                if en_content != cn_content and en_content == cn_content.strip():
                    if print_msg:
                        print(u'翻译中引号中的内容带有空格，删除')
                    cn = cn.replace('\'' + cn_content + '\'', '\'' + cn_content.strip() + '\'')
                    cn_content_with_quotation = cn_content.strip()
                else:
                    cn_content_with_quotation = cn_content
                cn_content_with_quotation = '\'' + cn_content_with_quotation + '\''
                if not cn.startswith(cn_content_with_quotation) and ' ' + cn_content_with_quotation not in cn:
                    cn = cn.replace(cn_content_with_quotation, ' ' + cn_content_with_quotation)
                if not cn.endswith(cn_content_with_quotation) and cn_content_with_quotation + ' ' not in cn:
                    cn = cn.replace(cn_content_with_quotation, cn_content_with_quotation + ' ')
        return cn

    @staticmethod
    def inspect_double_quote(en, cn, print_msg=False):
        """
        检查""，不使用“”，删去中间的空格
        """
        pattern = r'"(.+?)"'
        en_match = re.search(pattern, en)
        if en_match is not None:
            en_content = en_match.group(1)
            if print_msg:
                print(u'【%s】包含双引号，翻译是【%s】,内容是【%s】' % (en, cn, en_content))
            if en.count('"') == cn.count(u'“') * 2 and en.count('"') == cn.count(u'”') * 2:
                if print_msg:
                    print(u'【""】被翻译成了【“”】，替换')
                cn = cn.replace(u'“', '\"')
                cn = cn.replace(u'”', '\"')
            else:
                if print_msg:
                    print(u'%s 中双引号数量不匹配 %s' % (cn, en))
            cn_match_list = re.findall(pattern, cn)
            if cn_match_list:
                for cn_content in cn_match_list:
                    cn_content_strip = cn_content.replace(' ', '')
                    if cn_content not in en and cn_content_strip in en:
                        if print_msg:
                            print(u'翻译中引号中的内容带有空格，删除')
                        cn = cn.replace(cn_content, cn_content_strip)
        return cn


class StandardTranslation:
    """
    标准的翻译，可用,分隔
    英文|中文|不使用|备注
    """

    standard_translation_file = r'D:\workspace\BlogX\Chinglish\AndroidStudio\[2375]AndroidStudio汉化中使用的统一翻译.txt'
    standard_translation = list()

    def __init__(self, en, cn, replace):
        self.en_list = en.split(',')
        self.cn_list = cn.split(',')
        if replace:
            self.replace_list = replace.split(',')
        else:
            self.replace_list = []

    @staticmethod
    def get_standard_translation():
        """
        获取标准翻译
        """
        result = list()
        with open(StandardTranslation.standard_translation_file, encoding='utf-8') as file:
            all_lines = file.readlines()
            for line in all_lines:
                # 取小写
                line = line.rstrip('\n').lower()
                if '|' in line:
                    split_result = line.split('|')
                    en = split_result[0]
                    if len(split_result) > 1:
                        cn = split_result[1]
                    else:
                        cn = en
                    if len(split_result) > 2:
                        replace = split_result[2]
                    else:
                        replace = None
                    if en != '-':
                        result.append(StandardTranslation(en, cn, replace))
        return result

    @staticmethod
    def inspect_translation(en, cn, print_msg=False):
        """
        检查翻译是否准确，是否使用统一的翻译
        """
        if en == cn:
            # 如果相等根本没翻译就不检查了
            return cn
        en = en.lower()
        if not StandardTranslation.standard_translation:
            StandardTranslation.standard_translation = StandardTranslation.get_standard_translation()
        for standard_translation in StandardTranslation.standard_translation:
            for s_en in standard_translation.en_list:
                # 可能含标点符号，用空格分不准确
                if s_en in en.split(' '):
                    contain = False
                    for s_cn in standard_translation.cn_list:
                        if s_cn in cn:
                            contain = True
                            break
                    if not contain:
                        has_replace = False
                        if standard_translation.replace_list:
                            for replace in standard_translation.replace_list:
                                # 可能不只有一个
                                if cn.count(replace) == 1:
                                    # 只有一个，进行替换

                                    ignore_list = [
                                        r'just right-click an annotation',
                                    ]
                                    contain_ignore_word = False
                                    for ignore_word in ignore_list:
                                        if ignore_word in en:
                                            contain_ignore_word = True
                                            break
                                    if not contain_ignore_word:
                                        print(u'\n应该将【%s】替换为【%s】' % (replace, standard_translation.cn_list[0]))
                                        print(en)
                                        print(cn)
                                    # 不再直接替换,提醒操作
                                    # cn = cn.replace(replace, standard_translation.cn_list[0])
                                    has_replace = True
                        if not has_replace:
                            ignore_list = [
                                r'all you have to do',
                                r'<s3>view | parameter info</s3>',
                            ]
                            contain_ignore_word = False
                            for ignore_word in ignore_list:
                                if ignore_word in en:
                                    contain_ignore_word = True
                                    break
                            if not contain_ignore_word:
                                print(u'\n【%s】的翻译\n【%s】中不包含期望的翻译\n【%s】应该翻译为【%s】' % (
                                    en, cn, s_en, ','.join(standard_translation.cn_list)))

        return cn


if __name__ == '__main__':
    TranslationInspection().main()
