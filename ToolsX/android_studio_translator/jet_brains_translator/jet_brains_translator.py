import os
import shutil
import zipfile

from xx import filex
from xx import iox

from android_studio_translator.tips.tips import Tips
from android_studio_translator.tools import Tools
from android_studio_translator.translator.translation_file import TranslationFile


class JetBrainsTranslator:
    """汉化多个软件"""

    def __init__(self):
        self.work_dir = r'D:\workspace\TranslatorX\JetBrains'
        self.source_dir = self.work_dir + os.path.sep + 'source'
        self.target_dir = self.work_dir + os.path.sep + 'target'
        self.software_list = [
            Software(r'D:\xx\software\program\android\AndroidStudio', None, '3.0'),
            Software(r'D:\xx\software\JetBrains\IntelliJ IDEA Community Edition 2017.3', 'IntelliJIDEA',
                     '2017.3'),
            Software(r'D:\xx\software\JetBrains\PhpStorm 2017.3'),
            Software(r'D:\xx\software\JetBrains\PyCharm 2017.3'),
            Software(r'D:\xx\software\JetBrains\WebStorm 2017.3'),
        ]
        # 设置 work_dir
        for software in self.software_list:
            software.set_work_dir(self.work_dir)

    def main(self):
        action_list = [
            ['退出', exit],
            ['处理清单文件，整理tips的名称方便翻译', self.process_tips_manifest_file],
            ['检查并补全缺少的tips名', self.check_and_append_tips_name],
            ['将翻译结果的unicode转为中文', self.change_unicode_to_chinese],
            ['处理tips翻译结果为AndroidStudio用', self.process_tips_translation_result],
            ['重命名_zh_CN', self.rename_cn_files],
            ['复制 resources_en.jar', self.iter_software, lambda x: x.copy_resources_en_jar()],
            ['压缩进汉化包', self.iter_software, lambda x: x.zip_translation()],
            ['将汉化包复制到软件目录', self.iter_software, lambda x: x.copy_translation_to_work_dir()],
        ]
        iox.choose_action(action_list)

    def process_tips_manifest_file(self):
        tips = Tips()
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.source_dir + os.sep + project_name
            if os.path.isdir(project_path):
                tips_file_path = project_path + os.sep + 'IdeTipsAndTricks' + os.sep + 'IdeTipsAndTricks.xml'
                tips_en_file = filex.get_result_file_name(tips_file_path, '_en', 'properties')
                if os.path.exists(tips_file_path):
                    print('处理 %s' % tips_file_path)
                    tips.process_tips_manifest_file(tips_file_path, tips_en_file)

    def check_and_append_tips_name(self):
        tips = Tips()
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.source_dir + os.sep + project_name
            if os.path.isdir(project_path):
                tips_file_path = project_path + os.sep + 'IdeTipsAndTricks' + os.sep + 'IdeTipsAndTricks.xml'
                tips_en_file = filex.get_result_file_name(tips_file_path, '_en', 'properties')
                if os.path.exists(tips_file_path):
                    print('处理 %s' % tips_file_path)
                    project_tips_path = project_path + os.sep + 'resources_en' + os.sep + 'tips'
                    tips.check_and_append_tips_name(project_tips_path, tips_en_file, tips_en_file)

    def change_unicode_to_chinese(self):
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.target_dir + os.sep + project_name
            if os.path.isdir(project_path):
                tips_dir = project_path + os.sep + 'IdeTipsAndTricks'
                tips_file_path = tips_dir + os.sep + 'IdeTipsAndTricks_en_zh_CN.properties'
                tips_cn_file_path = tips_dir + os.sep + 'IdeTipsAndTricks_cn.properties'
                if os.path.exists(tips_file_path):
                    print('处理 %s' % tips_file_path)
                    Tools.change_unicode_to_chinese(tips_file_path, tips_cn_file_path)

    def process_tips_translation_result(self):
        tips = Tips()
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.target_dir + os.sep + project_name
            if os.path.isdir(project_path):
                tips_dir = project_path + os.sep + 'IdeTipsAndTricks'
                tips_cn_file_path = tips_dir + os.sep + 'IdeTipsAndTricks_cn.properties'
                if os.path.exists(tips_cn_file_path):
                    print('处理 %s' % tips_cn_file_path)
                    project_tips_path = project_path + os.sep + 'resources_en' + os.sep + 'tips'
                    tips.process_tips_translation_result(tips_cn_file_path, project_tips_path,
                                                         Tips.RESULT_TYPE_ANDROID_STUDIO, project_tips_path)

    def rename_cn_files(self):
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.target_dir + os.sep + project_name
            if os.path.isdir(project_path):
                project_messages_path = project_path + os.sep + 'resources_en' + os.sep + 'messages'
                TranslationFile.rename_cn_files(project_messages_path)

    def iter_software(self, callback):
        """对所有软件循环进行操作"""
        for software in self.software_list:
            callback(software)


class Software:
    def __init__(self, path, name=None, version=None, release_version=1):
        self.work_dir = ''
        "汉化包的工作目录"
        self.path = path
        "软件的安装目录"
        base_name = os.path.basename(path)
        if name is None or version is None:
            name_version = base_name.split(' ')
            if len(name_version) > 0:
                if name is None:
                    name = name_version[0]
            if len(name_version) > 1:
                if version is None:
                    version = name_version[1]
        self.name = name
        "软件名"
        self.version = version
        "软件版本"
        self.release_version = release_version
        "当前软件版本下的汉化包版本，如果需要，可以手动设置，分开设置"
        self.en_jar_path = ''
        "软件的英文包"
        self.translation_jar_name = 'resources_cn_%s_%s_r%s.jar' % (self.name, self.version, self.release_version)
        "汉化包言语件名"
        self.translation_jar = ''
        "汉化包完整路径"

    def set_work_dir(self, work_dir):
        self.work_dir = work_dir
        self.translation_jar = '%s/jars/%s/%s' % (self.work_dir, self.name, self.translation_jar_name)
        self.en_jar_path = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.version, 'resources_en.jar')

    def copy_resources_en_jar(self):
        """复制 jar"""
        print('处理 %s %s' % (self.name, self.version))
        if not os.path.exists(self.path):
            print('软件目录不存在 %s' % self.path)
            return
        jar_file_path = self.path + os.sep + 'lib' + os.sep + 'resources_en.jar'
        if not os.path.exists(jar_file_path):
            print('jar 包不存在')
            return
        print('复制 %s 到 %s' % (jar_file_path, self.en_jar_path))
        filex.check_and_create_dir(self.en_jar_path)
        shutil.copyfile(jar_file_path, self.en_jar_path)

    def zip_translation(self):
        """打包翻译"""
        print('处理 %s %s' % (self.name, self.version))
        translation_dir = '%s/target/%s/resources_en' % (self.work_dir, self.name)
        print('将 %s 压缩到 %s' % (translation_dir, self.translation_jar))
        self.zip(translation_dir, self.translation_jar, self.en_jar_path)

    @staticmethod
    def zip(source_dir, target_jar, source_jar=None):
        if os.path.exists(target_jar):
            os.remove(target_jar)
        if source_jar is not None:
            translation_dir_list = []
            translation_file_list = []
            for root, dirs, files in os.walk(source_dir):
                for dir_name in dirs:
                    path = root + '/' + dir_name
                    translation_dir_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
                for file_name in files:
                    path = root + '/' + file_name
                    translation_file_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
            print(translation_dir_list)
            print(translation_file_list)
            tmp_dir = os.path.splitext(source_jar)[0]
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            # 解压仅存在于 source_jar 中的内空
            print('解压缺少的文件')
            with zipfile.ZipFile(source_jar, 'r') as zip_file:
                for name in zip_file.namelist():
                    for translation_dir in translation_dir_list:
                        if name.startswith(translation_dir):
                            if name not in translation_file_list:
                                # print('翻译文件中缺少 %s ，解压缩' % name)
                                zip_file.extract(name, tmp_dir)
            print('压缩缺少的文件')
            ZipTools.zip_jar(tmp_dir, target_jar)
            # 删除
            print('删除临时文件 %s' % tmp_dir)
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
        # 压缩翻译内容
        ZipTools.zip_jar(source_dir, target_jar)

    def copy_translation_to_work_dir(self):
        """复制汉化包到工作目录"""
        jar_file_path = self.path + os.sep + 'lib' + os.sep + self.translation_jar_name
        print('复制 %s 到 %s' % (self.translation_jar, jar_file_path))
        shutil.copyfile(self.translation_jar, jar_file_path)


class ZipTools:
    @staticmethod
    def zip_jar(source_dir, target_jar):
        """压缩文件夹"""
        print('压缩 %s 到 %s' % (source_dir, target_jar))
        filex.check_and_create_dir(target_jar)
        translation_file_list = []
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                path = root + '/' + file_name
                translation_file_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
        with zipfile.ZipFile(target_jar, 'a') as zip_file:
            for file in translation_file_list:
                # print('压缩 %s' % file)
                zip_file.write(source_dir + os.sep + file, file)


if __name__ == '__main__':
    JetBrainsTranslator().main()
