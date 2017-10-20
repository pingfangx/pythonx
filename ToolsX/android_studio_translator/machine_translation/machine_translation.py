import json
import re
import subprocess
import urllib.parse
from abc import ABC, abstractmethod
from xml.etree import ElementTree as Et

from xx import filex
from xx import iox
from xx import netx

from android_studio_translator.machine_translation.Py4Js import Py4Js
from android_studio_translator.machine_translation.google_tk import get_google_tk
from android_studio_translator.tools import Tools
from android_studio_translator.translation_inspection.translation_inspection import TranslationInspection


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
            exit()
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
                # 第 1 个带翻译，第 2 个可能带拼音
                translation = first_result[0]
                # 翻译中的第一个即是结果
                cn = translation[0]
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
        all_match = re.findall(r'(?<!\s)<(\w+?)>\s(.+?)\s</\1>(?!\s)', cn)
        if all_match:
            for (tag, content) in all_match:
                find = r'<%s> %s </%s>' % (tag, content, tag)
                # 有时[0]前会被谷歌加上空格
                content = re.sub(r'\s(\[\d\])', r'\1', content)
                replace = r' <%s>%s</%s> ' % (tag, content, tag)
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
        project_dir = r'D:\workspace\WebsiteCopy\Translation'
        pseudo_file = 'pseudo.tmx'
        ignore_reg_list = [
            r'^[\.[<#$-]|[\u4e00-\u9fa5]|git|GIT|http'
        ]
        """
        \. 上一级目录
        [ 可选参数
        < 标签或参数
        # 锚点
        $ 命仅
        - -- 参数
        [\u4e00-\u9fa5] 中文
        git GIT 命令
        http https 链接
        """
        action_list = [
            ['退出', exit],
            ['生成伪翻译记忆文件', self.create_pseudo_translation, omegat_file_path, project_dir, pseudo_file, 'empty'],
            ['谷歌翻译记忆文件', self.translate_file, GoogleTranslator, pseudo_file, ignore_reg_list],
            ['百度翻译记忆文件', self.translate_file, BaiduTranslator, pseudo_file, ignore_reg_list],
            ['删除空翻译', self.delete_empty_translation, pseudo_file],
            ['测试 tk', self.test_tk, 'See <a0>gitnamespaces[7]</a0> for more details.'],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def test_tk(a='test'):
        print(Py4Js().getTk(a))
        print(get_google_tk(a))
        print(GoogleTranslator.translate(a))

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

    @staticmethod
    def translate_file(cls, file_path, ignore_reg_list):
        """
        翻译
        寻找一个要翻译的单词
        翻译，更新字典，保存
        继续
        :param cls: 类
        :param file_path: 文件路径
        :param ignore_reg_list: 忽略正则列表，如果匹配则忽略
        :return: 
        """

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
                    if re.match(ignore_reg, en):
                        print('\n跳过 %d/%d 个:【%s】' % (i + 1, length, en))
                        continue_loop = True
                        break
            if continue_loop:
                continue
            print('\n翻译 %d/%d 个:【%s】' % (i + 1, length, en))
            cn = cls.translate(en)
            print('翻译结果 %d/%d 个:【%s】' % (i + 1, length, cn))
            # 更新字典
            en_dict[en] = cn
            # 写入文件
            MachineTranslation.save_translation(file_path, en, cn)

    @staticmethod
    def delete_empty_translation(file_path):
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
            if not cn:
                empty_translation_list.append(tu)
            if en == cn:
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
