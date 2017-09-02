import re

from android_studio_translator.keymap.tools import Tools
from xx import filex
from xx import iox


class ActionBundle:
    def main(self):
        # 1补充过的英文文件,并且删除等号左右两边的空格
        en_add_file = 'bundle/ActionsBundle_en_add.properties'
        # 4修改断句的文件
        cn_split_file = 'bundle/ActionsBundle_cn_split.properties'
        # 中文修改过的文件，删除快捷方式，删除末尾的.或省略号
        cn_modified_file = 'bundle/ActionsBundle_cn_modified.properties'
        # 翻译结果文件
        en_modified_add_translation_file = r"D:\workspace\TranslatorX\AndroidStudio\target" \
                                           r"\ActionsBundle_en_add_modified_zh_CN.properties "
        action_list = [
            ['退出', exit],
            ['处理' + en_add_file, self.process_file_for_translation, en_add_file],
            ['处理' + cn_split_file, self.process_file_for_translation, cn_split_file,
             cn_modified_file],
            ['处理翻译结果', self.add_ellipsis_and_shortcut, en_add_file, en_modified_add_translation_file],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def process_file_for_translation(file, result_file=None):
        """
        在翻译前处理文件
        删除快捷方式
        删除末尾的.或省略号
        :param file:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(file, '_modified')
        print('删除省略号')
        Tools.delete_symbol(file, 0, 0, result_file)
        # 后面的将接着用result_fiel
        print('删除快捷方式')
        Tools.delete_symbol(result_file, 0, 1, result_file)
        print('删除等号前后的空格')
        Tools.delete_symbol(result_file, 0, 2, result_file)
        print('再次删除省略号，防止位于快捷方式之前')
        Tools.delete_symbol(result_file, 0, 0, result_file)

    @staticmethod
    def add_ellipsis_and_shortcut(en_file, cn_file, result_file=None):
        """
        处理快捷键，将_字母替换为(_字母)
        :param en_file:
        :param cn_file:
        :param result_file:
        :return:
        """
        if result_file is None:
            result_file = filex.get_result_file_name(cn_file, '_add_ellipsis_and_shortcut')

        en_dict = Tools.get_dict_from_file(en_file, delete_value_ellipsis=False, delete_value_underline=False)
        cn_dict = Tools.get_dict_from_file(cn_file, delete_value_ellipsis=False, delete_value_underline=False)
        count = 0

        p_ellipsise = re.compile('……|…$')
        p_period = re.compile('\.')
        for (k, v) in en_dict.items():
            if v.endswith('.'):
                # 以.结尾
                if k in cn_dict.keys():
                    cn_value = cn_dict[k]
                    old_value = cn_value
                    if v.endswith('...'):
                        # 省略号结尾
                        cn_value = re.sub(p_ellipsise, '...', cn_value)
                        if not cn_value.endswith('...'):
                            cn_value += '...'
                    elif v.endswith('.'):
                        # 句号结尾
                        cn_value = re.sub(p_period, '。', cn_value)
                        if not cn_value.endswith('。'):
                            cn_value += '。'

                    if cn_value != old_value:
                        print('修改【%s】为【%s】' % (old_value, cn_value))
                        cn_dict[k] = cn_value
            if '_' in v:
                # 有快捷方式
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
        result = Tools.translate_file_by_dict(en_file, cn_dict, '')  # 重新翻译
        filex.write_lines(result_file, result)


if __name__ == '__main__':
    ActionBundle().main()
