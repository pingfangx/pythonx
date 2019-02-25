import json
import re
import shutil
import subprocess
import urllib.parse
from abc import ABC, abstractmethod
from xml.etree import ElementTree as Et

import pyperclip

from tool.android.android_studio_translator.machine_translation.Py4Js import Py4Js
from tool.android.android_studio_translator.machine_translation.google_tk import get_google_tk
from tool.android.android_studio_translator.tools import Tools
from tool.android.android_studio_translator.translation_inspection.translation_inspection import TranslationInspection
from xx import filex
from xx import iox
from xx import netx


class MachineTranslator(ABC):
    """翻译抽象类"""

    @staticmethod
    @abstractmethod
    def translate(en):
        """翻译"""


class GoogleTranslator(MachineTranslator):
    """谷歌翻译"""

    @staticmethod
    def translate(en):
        js = Py4Js()
        tk = js.getTk(en)
        tk2 = get_google_tk(en)
        if tk != tk2:
            print('计算的 tk 不相等')
            filex.write('data/error_tk.txt', en + '\n', 'a')
            return en
        url = "http://translate.google.cn/translate_a/single?client=t" \
              "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
              "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
              "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, urllib.parse.quote(en))
        result = netx.get(url, need_print=False)
        """
        [[["测试","test",null,null,2],[null,null,"Cèshì","test"]],...]
        """
        if result:
            result = json.loads(result)
            if result:
                # 第一个结果
                first_result = result[0]
                # 前几个为翻译，最后 1 个可能带拼音
                cn = ''
                for translation in first_result:
                    if len(translation) == 5:
                        # 翻译中的第一个即是结果
                        cn += translation[0]
                cn = GoogleTranslator.process_result(en, cn)
                return cn
        return None

    @staticmethod
    def process_result(en, cn):
        """处理结果"""
        # 标签会被加上空格，将空格去除
        all_match = re.findall('</ .+?>', cn)
        if all_match:
            for match in all_match:
                without_space = match.replace(' ', '')
                if without_space in en and match not in en:
                    # 在 en 中有不含空格的，没有含空格的，才替换
                    cn = cn.replace(match, without_space)
        # 谷歌翻译标签前后会被加上空格
        # 匹配<tag>空格内容空格</tag>
        all_match = re.findall(r'<(\w+?)>(.+?)</\1>', cn)
        if all_match:
            for (tag, content) in all_match:
                en_match = re.search(r'<%s>(.+?)</%s>' % (tag, tag), en)
                if not en_match:
                    print('tag 不正确,cn=【%s】,en=【%s】,tag=【%s】' % (cn, en, tag))
                    exit()
                en_content = en_match.group(1)
                # 增加前后空格
                if not cn.startswith(r'<%s>' % tag):
                    cn = re.sub(r'\s?(<%s>)' % tag, r' \1', cn)
                if not cn.endswith(r'</%s>' % tag):
                    cn = re.sub(r'(</%s>)\s?' % tag, r'\1 ', cn)
                # 将翻译替换为英文，保持原样
                find = r'<%s>%s</%s>' % (tag, content, tag)
                replace = r'<%s>%s</%s>' % (tag, en_content, tag)
                # 将中间的空格替换为前后的空格，这里不能用正则，因为内容中可能有符号
                cn = cn.replace(find, replace)
        cn = TranslationInspection.inspect(en, cn)
        return cn


class BaiduTranslator(MachineTranslator):
    """百度翻译"""

    @staticmethod
    def translate(en):
        return '百度翻译'


class MachineTranslation:
    def main(self):
        omegat_file_path = r'D:\xx\software\program\OmegaT_4.1.2_01_Beta_Without_JRE\OmegaT2.jar'
        project_dir = r'D:\workspace\TranslatorX\test'
        pseudo_file = 'data/pseudo.tmx'
        translation_file = 'data/translation.tmx'
        ignore_file = 'data/auto.tmx'
        ignore_reg_list = [
            r'^[\.[#$-]|git|GIT|http|android[\.:]',
            r'[\u4e00-\u9fa5]',
        ]
        """
        \. 上一级目录
        [ 可选参数
        # 锚点
        $ 命仅
        - -- 参数
        [\u4e00-\u9fa5] 中文
        git GIT 命令
        http https 链接
        android. 和 android:
        """
        action_list = [
            ['退出', exit],
            ['生成伪翻译记忆文件并复制替换 auto translation', self.create_pseudo_translation, omegat_file_path, project_dir,
             pseudo_file, 'empty'],
            ['过滤 translation.tmx', self.filter, translation_file, ignore_reg_list, translation_file],
            ['谷歌翻译记忆文件 并删除空翻译', self.translate_file, GoogleTranslator, translation_file, translation_file,
             ignore_reg_list,
             None, True],
            ['百度翻译记忆文件', self.translate_file, BaiduTranslator, pseudo_file, translation_file, ignore_reg_list,
             ignore_file],
            ['删除 translation 空翻译', self.delete_empty_or_same_translation, translation_file],
            ['删除 auto 空翻译', self.delete_empty_or_same_translation, ignore_file, True, False],
            ['测试 tk', self.test_tk, r'a valid tag <e0>name</e0> (i.e. a <c1>refs/tags/<tag></c1> reference).'],
            ['读取输入并翻译', self.read_and_translate],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def filter(file_path, ignore_reg_list, result_path=None):
        """过滤掉不需要翻译的"""
        if result_path is None:
            result_path = filex.get_result_file_name(file_path, '_filter')

        """删除空翻译"""
        tree = Et.parse(file_path)
        tmx = tree.getroot()
        body = tmx.find('body')

        empty_translation_list = list()
        for tu in body.iter('tu'):
            en = None
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'EN-US':
                    en = tuv.find('seg').text
            continue_loop = False
            if ignore_reg_list:
                for ignore_reg in ignore_reg_list:
                    if ignore_reg.startswith('^'):
                        if re.match(ignore_reg, en):
                            continue_loop = True
                    else:
                        # 不以 ^ 开头才搜索
                        if re.search(ignore_reg, en):
                            continue_loop = True
                    if continue_loop:
                        print('\n跳过【%s】' % en)
                        empty_translation_list.append(tu)
                        break
            if continue_loop:
                continue
        print('删除 %d 条空翻译' % len(empty_translation_list))
        for empty_translation in empty_translation_list:
            body.remove(empty_translation)
        tree.write(result_path, encoding='utf-8')
        print('保存完成')

    @staticmethod
    def read_and_translate():
        """读取并翻译"""
        hint = '\n请输入要翻译的内空\t(0 表示退出)\n'
        word = input(hint)
        while word != '0':
            print('翻译中...')
            translation = GoogleTranslator.translate(word)
            pyperclip.copy(translation)
            print('已翻译并复制【%s】' % translation)
            word = input(hint)

    @staticmethod
    def test_tk(a='test'):
        print(Py4Js().getTk(a))
        print(get_google_tk(a))
        translation = GoogleTranslator.translate(a)
        pyperclip.copy(translation)
        print('已翻译并复制【%s】' % translation)

    @staticmethod
    def create_pseudo_translation(jar_file, project_dir, result_file=None, translate_type='empty'):
        """
        创建伪翻译
        java -jar OmegaT.jar <project-dir> --mode=console-createpseudotranslatetmx --pseudotranslatetmx=<filename>
         --pseudotranslatetype=[equal|empty]
        :param jar_file:  OmegaT 的 jar 文件
        :param project_dir:  项目目路
        :param result_file: 结果文件，tmx 格式
        :param translate_type: 翻译类型，可选 equal | empty
        :return: 
        """
        if result_file is None:
            result_file = filex.get_result_file_name('pseudo', '', 'tmx')
        cmd = 'java -jar %s %s --mode=console-createpseudotranslatetmx --pseudotranslatetmx=%s ' \
              '--pseudotranslatetype=%s' % (jar_file, project_dir, result_file, translate_type)
        print(cmd)
        subprocess.call(cmd, shell=True)
        print('已输出文件 %s' % result_file)

        auto_file = 'data/auto.tmx'
        shutil.copyfile(result_file, auto_file)
        print('已复制文件 %s' % auto_file)

        translation_file = 'data/translation.tmx'
        shutil.copyfile(result_file, translation_file)
        print('已复制文件 %s' % translation_file)

    @staticmethod
    def translate_file(cls, file_path, result_file=None, ignore_reg_list=None, ignore_file_path=None,
                       delete_empty_translation=False):
        """
        翻译
        寻找一个要翻译的单词
        翻译，更新字典，保存
        继续
        :param cls: 类
        :param file_path: 文件路径
        :param result_file: 结果文件
        :param ignore_reg_list: 忽略正则列表，如果匹配则忽略
        :param ignore_file_path: 忽略的单词保存于，用于生成 auto中的tmx ，避免每次都要手动设为相同翻译
        :param delete_empty_translation: 删除空翻译
        :return: 
        """

        if result_file is None:
            result_file = file_path

        if not issubclass(cls, MachineTranslator):
            print('%s 不是 MachineTranslator 的子类' % cls)
            return

        en_dict = Tools.get_dict_from_omegat(file_path)
        if not en_dict:
            print('翻译文件字典为空')
            return

        keys = sorted(en_dict.keys())
        length = len(keys)
        for i in range(length):
            en = keys[i]
            cn = en_dict[en]
            if cn is not None:
                continue
            continue_loop = False
            if ignore_reg_list:
                for ignore_reg in ignore_reg_list:
                    if ignore_reg.startswith('^'):
                        if re.match(ignore_reg, en):
                            continue_loop = True
                    else:
                        # 不以 ^ 开头才搜索
                        if re.search(ignore_reg, en):
                            continue_loop = True
                    if continue_loop:
                        print('\n跳过 %d/%d 个:【%s】' % (i + 1, length, en))
                        if ignore_file_path:
                            MachineTranslation.save_translation(ignore_file_path, en, en)
                        break
            if continue_loop:
                continue
            print('\n翻译 %d/%d 个:【%s】' % (i + 1, length, en))
            cn = cls.translate(en)
            print('翻译结果 %d/%d 个:【%s】' % (i + 1, length, cn))
            # 更新字典
            en_dict[en] = cn
            # 写入文件
            MachineTranslation.save_translation(result_file, en, cn)
        if delete_empty_translation:
            MachineTranslation.delete_empty_or_same_translation(result_file, True, True)

    @staticmethod
    def delete_empty_or_same_translation(file_path, delete_empty=True, delete_same=True):
        """删除空翻译"""
        tree = Et.parse(file_path)
        tmx = tree.getroot()
        body = tmx.find('body')

        empty_translation_list = list()
        for tu in body.iter('tu'):
            en = None
            cn = None
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'ZH-CN':
                    cn = tuv.find('seg').text
                if tuv.attrib['lang'] == 'EN-US':
                    en = tuv.find('seg').text
            if delete_empty and not cn:
                empty_translation_list.append(tu)
            if delete_same and en == cn:
                empty_translation_list.append(tu)
        print('删除 %d 条空翻译' % len(empty_translation_list))
        for empty_translation in empty_translation_list:
            body.remove(empty_translation)
        tree.write(file_path, encoding='utf-8')
        print('保存完成')

    @staticmethod
    def save_translation(file_path, check_en, save_cn):
        """保存翻译"""

        tree = Et.parse(file_path)
        tmx = tree.getroot()
        body = tmx.find('body')
        for tu in body.iter('tu'):
            en = None
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'EN-US':
                    en = tuv.find('seg').text
                    break
            # 检查
            if en is None or en != check_en:
                continue
            # 保存
            for tuv in tu.iter('tuv'):
                if tuv.attrib['lang'] == 'ZH-CN':
                    tuv.find('seg').text = save_cn
                    tree.write(file_path, encoding='utf-8')
                    print('保存完成【%s】:【%s】' % (check_en, save_cn))
                    return


if __name__ == '__main__':
    MachineTranslation().main()
