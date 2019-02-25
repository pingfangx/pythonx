import re

from tool.android.android_studio_translator.delete_action import DeleteAction
from tool.android.android_studio_translator.tools import Tools
from xx import filex
from xx import iox


# from android_studio_translator.tips.tips import Tips


class ActionsBundle:
    """
    AndroidStudio的ActionsBundle
    [AndroidStudio翻译(3)-ActionsBundle中文翻译](http://blog.pingfangx.com/2355.html)
    """
    en_add_file = 'data/ActionsBundle_en_add.properties'
    """只是添加了几个语句，保留快捷键和省略号"""

    en_add_modified_translation_file = r"D:\workspace\TranslatorX\AndroidStudio\target" \
                                       r"\ActionsBundle_en_add_modified_zh_CN.properties "
    """处理完快捷键和省略，翻译结果文件"""

    def main(self):
        version = '2.3.3'
        "版本号"

        project_dir = r'D:\workspace\TranslatorX\AndroidStudio'
        "项目路径"

        source_dir = project_dir + r'\source'
        "OmegaT的source路径"
        target_dir = project_dir + r'\target'
        "OmegaT的target路径"
        original_dir = project_dir + r'\original'

        source_messages_dir = r'%s\%s\%s' % (source_dir, version, r'lib\resources_en\messages')
        target_messages_dir = r'%s\%s\%s' % (target_dir, version, r'lib\resources_en\messages')
        original_message_dir = r'%s\%s\%s' % (original_dir, version, r'lib\resources_en\messages')

        name_pattern = r'.properties'
        """处理时过滤文件的模板"""

        en_add_file = ActionsBundle.en_add_file
        cn_split_file = 'data/ActionsBundle_cn_split.properties'
        """修改断句的文件"""

        cn_modified_file = 'data/ActionsBundle_cn_modified.properties'
        """中文修改过的文件，删除快捷方式，删除末尾的.或省略号"""

        en_modified_add_translation_file = ActionsBundle.en_add_modified_translation_file

        result_file = r"data/ActionsBundle_result.properties"

        omegat_dict_file = project_dir + r'/omegat/project_save.tmx'
        "记忆库文件"
        pseudo_dict_file = original_message_dir + r'.tmx'
        "伪翻译记忆"

        action_list = [
            ['退出', exit],
            ['处理' + en_add_file, self.process_file_for_translation, en_add_file],
            ['处理' + cn_split_file, self.process_file_for_translation, cn_split_file, cn_modified_file],
            ['处理翻译结果', self.add_ellipsis_and_shortcut, en_add_file, en_modified_add_translation_file, result_file],
            ['处理所有文件' + original_message_dir, self.process_dir_for_translation, original_message_dir,
             source_messages_dir,
             name_pattern],
            ['处理所有文件的翻译结果' + target_dir, self.process_dir_translation_result, original_message_dir, target_messages_dir,
             None, name_pattern],
            ['根据伪翻译文件更新记忆库', self.update_omegat_dict_by_pseudo_dict, omegat_dict_file, pseudo_dict_file],
            ['将谷歌翻译文件处理为记忆库', self.process_google_translation_to_omegat_dict,
             r"D:\workspace\TranslatorX\AndroidStudio\source\2.3.3\plugins\android\lib\resources_en\messages\AndroidBundle_modified.properties",
             r"D:\workspace\TranslatorX\AndroidStudio\source\2.3.3\plugins\android\lib\resources_en\messages\1.txt"]
        ]
        iox.choose_action(action_list)

    @staticmethod
    def process_dir_for_translation(process_dir, result_dir=None, name_pattern=None):
        """处理文件夹中的所有文件"""
        if result_dir is None:
            result_dir = process_dir + '_delete'
        file_list = filex.list_file(process_dir, name_pattern)
        length = len(file_list)
        for i in range(length):
            file = file_list[i]
            print('process %d/%d' % (i + 1, length))
            result_file = file.replace(process_dir, result_dir)
            ActionsBundle.process_file_for_translation(file, result_file)

    @staticmethod
    def process_dir_translation_result(en_dir, cn_dir, result_dir=None, name_pattern=None):
        """处理文件夹中的所有文件"""
        if result_dir is None:
            result_dir = cn_dir + '_add'

        en_file_list = filex.list_file(en_dir, name_pattern)
        length = len(en_file_list)
        for i in range(length):
            en_file = en_file_list[i]
            print('process %d/%d' % (i + 1, length))
            cn_file = en_file.replace(en_dir, cn_dir)
            cn_file = filex.get_result_file_name(cn_file, '_zh_CN')
            result_file = en_file.replace(en_dir, result_dir)
            ActionsBundle.add_ellipsis_and_shortcut(en_file, cn_file, result_file)

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
        DeleteAction.delete_ellipsis(file, result_file)
        # 后面的将接着用result_fiel
        print('删除快捷方式')
        DeleteAction.delete_underline_shortcut(result_file, result_file)
        print('删除&形式的快捷方式')
        DeleteAction.delete_and_shortcut(result_file, result_file)
        print('再次删除省略号，防止位于快捷方式之前')
        DeleteAction.delete_ellipsis(result_file, result_file)

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
        result.insert(0, '# from:[AndroidStudio翻译(3)-ActionsBundle中文翻译](http://blog.pingfangx.com/2355.html)\n')
        filex.write_lines(result_file, result)

    @staticmethod
    def update_omegat_dict_by_pseudo_dict(omegat_dict_file, pseudo_dict_file, result_file=None):
        "根据伪翻译记忆更新记忆库"
        if result_file is None:
            result_file = filex.get_result_file_name(pseudo_dict_file, '_update_by_pseudo')
        source_dict = Tools.get_dict_from_omegat(omegat_dict_file)
        pseudo_dict = Tools.get_dict_from_omegat(pseudo_dict_file)
        print('记忆库共%d条记录，伪翻译共%d条记录' % (len(source_dict), len(pseudo_dict)))
        result_dict = ActionsBundle.update_dict_add_extra_info(source_dict, pseudo_dict)
        print('处理结果共%s条记录' % len(result_dict))
        Tools.save_omegat_dict(result_dict, result_file)

    @staticmethod
    def update_dict_add_extra_info(source_dict, pseudo_dict):
        "更新词典，添加快捷键、结尾标点符号等"
        result_dict = dict()
        for en in pseudo_dict.keys():
            # 处理快捷键
            cn = None
            if 'Cannot add build files from excluded directories' in en:
                print('1')
            abbreviated_en = DeleteAction.delete_all_symbol_of_string(en, False)
            if abbreviated_en != en:
                # 只有缩短的才需要处理
                if abbreviated_en in source_dict.keys():
                    cn = source_dict[abbreviated_en]
                    cn = DeleteAction.add_extra_info_of_string(en, cn, False)
                else:
                    # print('不包含缩简key:%s' % abbreviated_en)
                    pass
            if cn is None:
                if en in source_dict.keys():
                    cn = source_dict[en]
                else:
                    print('不包含原始key:%s' % en)
            if cn is not None:
                result_dict[en] = cn
        return result_dict

    @staticmethod
    def process_google_translation_to_omegat_dict(en_file, cn_file, result_file=None):
        if result_file is None:
            result_file = filex.get_result_file_name(en_file, '', 'tmx')
        en_dict = filex.get_dict_from_file(en_file)
        cn_dict = filex.get_dict_from_file(cn_file)
        print('英文词典%d条' % (len(en_dict)))
        print('中文词典%d条' % (len(cn_dict)))

        result = dict()
        for cn_key, cn_value in cn_dict.items():
            cn_key = cn_key.strip()
            cn_value=cn_value.strip()
            if cn_key in en_dict.keys():
                en_value = en_dict[cn_key]
                result[en_value] = cn_value

        print('结果%d条' % (len(result)))
        Tools.save_omegat_dict(result, result_file)


if __name__ == '__main__':
    ActionsBundle().main()
