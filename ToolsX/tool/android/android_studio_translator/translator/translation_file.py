import filecmp
import os
import shutil
import zipfile

from tool.android.android_studio_translator import Version
from xx import filex
from xx import iox


class TranslationFile:
    """主要用要翻译后的处理文件
    打包jar包，
    备份、替换、还原j等
    """

    file_list = [
        'lib/idea.jar',
        'lib/resources.jar',
        'lib/resources_en.jar',
        'plugins/android/lib/android.jar',
        'plugins/android/lib/resources_en.jar',
    ]

    def main(self):
        source_dir = r'D:\xx\software\program\android\AndroidStudio'
        "源目录"

        backup_dir = r'D:\workspace\TranslatorX\AndroidStudio\original\%s' % Version.version
        "备份目录，不可修改，要用于备分"

        work_dir = r'D:\workspace\TranslatorX\AndroidStudio\result\%s' % Version.version
        "要替换的文件所在的目录"

        action_list = [
            ['退出', exit],
            ['备份文件,%s到%s' % (source_dir, backup_dir), self.copy_dir, source_dir, backup_dir],
            ['恢复文件,%s到%s' % (backup_dir, source_dir), self.copy_dir, backup_dir, source_dir],
            ['复制备份文件到工作目录,%s到%s' % (backup_dir, work_dir), self.copy_dir, backup_dir, work_dir],
            ['直接打包jar文件到源目录,%s到%s' % (work_dir, source_dir), self.jar_file, source_dir, work_dir],
            ['恢复备份并打包jar文件到源目录', self.restore_and_jar_file, backup_dir, source_dir, work_dir],
            ['打包jar文件到工作目录,%s到%s' % (work_dir, work_dir), self.jar_file, work_dir, work_dir],
            ['替换源文件,%s到%s' % (work_dir, source_dir), self.copy_dir, work_dir, source_dir],
            ['打包到工作目录并替换源目录', self.jar_file_and_replace, work_dir, work_dir, source_dir],
            ['根据翻译的jar包复制原始jar包', self.process_jar_by_translation, r'D:\workspace\汉化包\translation', source_dir,
             r'D:\workspace\汉化包\original'],
            ['解包所有jar包', self.unpack_all_jar, r'D:\workspace\汉化包\original'],
            ['根据汉化文件解包 jar 包', self.unpack_jar_by_translation_file, TranslationFile.file_list, work_dir,
             r'D:\xx\software\program\android\AndroidStudio-3.0.1-back'],
            ['重命名_zh_CN', self.rename_cn_files, work_dir],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def rename_cn_files(work_dir):
        """将翻译文件中的 _zh_CN删除，用于英文环境也可以正常使用"""
        for root, dirs, files in os.walk(work_dir):
            for file in files:
                if file.endswith('_zh_CN.properties'):
                    old_name = root + os.path.sep + file
                    new_name = old_name.replace('_zh_CN.properties', '.properties')
                    if os.path.exists(new_name):
                        print('delete 【%s】' % new_name)
                        os.remove(new_name)
                    print('rename 【%s】 to 【%s】' % (old_name, new_name))
                    os.rename(old_name, new_name)

    @staticmethod
    def copy_dir(source_dir, target_dir, file_list=None):
        """备份"""
        if file_list is None:
            file_list = TranslationFile.file_list
        for file in file_list:
            source_file = '%s/%s' % (source_dir, file)
            if not os.path.exists(source_file):
                print('文件不存在%s' % source_file)
                continue
            target_file = '%s/%s' % (target_dir, file)
            if os.path.exists(target_file):
                if filecmp.cmp(source_file, target_file):
                    print('文件已相同%s与%s' % (source_file, target_file))
                    continue
            filex.check_and_create_dir(target_file)
            shutil.copyfile(source_file, target_file)
            print('复制文件%s到%s' % (source_file, target_file))
        pass

    @staticmethod
    def restore_and_jar_file(backup_dir, source_dir, work_dir):
        """恢复备份并打包"""
        TranslationFile.copy_dir(backup_dir, source_dir)
        TranslationFile.jar_file(source_dir, work_dir)

    @staticmethod
    def jar_file(jar_file_dir, jar_content_dir):
        """
        打包jar文件
        本来也可以直接打包到源目录，但为了可以提供jar包，就打包到工作目录
        """
        for file in TranslationFile.file_list:
            source_file = '%s/%s' % (jar_file_dir, file)
            print('处理%s' % source_file)
            if not os.path.exists(source_file):
                print('文件不存在%s' % source_file)
                continue
            work_jar_file = '%s/%s' % (jar_content_dir, file)
            work_jar_dir = os.path.splitext(work_jar_file)[0]
            with zipfile.ZipFile(source_file, 'a') as zip_file:
                work_file_list = filex.list_file(work_jar_dir)
                print('压缩%d个文件' % len(work_file_list))
                for work_file in work_file_list:
                    # 相对于jar目录，所以替换
                    # 注意这里会导致文件重复
                    zip_file.write(work_file, arcname=work_file.replace(work_jar_dir, ''))

    @staticmethod
    def jar_file_and_replace(jar_file_dir, jar_content_dir, target_dir):
        """打包并替换"""
        TranslationFile.jar_file(jar_file_dir, jar_content_dir)
        TranslationFile.copy_dir(jar_file_dir, target_dir)

    @staticmethod
    def process_jar_by_translation(translation_dir, source_dir, target_dir):
        """根据汉化包备份包"""
        jar_files = filex.list_file(translation_dir)
        file_list = [jar_file.replace(translation_dir, '') for jar_file in jar_files]
        TranslationFile.copy_dir(source_dir, target_dir, file_list)

    @staticmethod
    def unpack_all_jar(dir_path):
        for file_path in filex.list_file(dir_path, '.jar$'):
            print('解包%s' % file_path)
            folder = os.path.splitext(file_path)[0]
            with zipfile.ZipFile(file_path) as zip_file:
                zip_file.extractall(folder)

    @staticmethod
    def unpack_jar_by_translation_file(jar_list, translation_dir, root_dir, output_dir=None):
        """
        根据汉化的文件，解压 jar 包，
        用于解压出要汉化的文件，或是比较有没有发生变化
        :param jar_list: 要处理的 jar 包
        :param translation_dir: 翻译文件的目录
        :param root_dir: jar 包根目录
        :param output_dir: 输出目录
        :return: 
        """
        if output_dir is None:
            output_dir = root_dir + '_unpack'
        for jar_file in jar_list:
            jar_file_path = root_dir + os.path.sep + jar_file
            print('\njar 文件 %s' % jar_file_path)
            if not os.path.exists(jar_file_path):
                print('jar 文件不存在：%s' % jar_file_path)
                continue

            translation_jar_dir = translation_dir + os.path.sep + jar_file.replace('.jar', '')
            print('翻译结果 %s' % translation_jar_dir)
            if not os.path.exists(translation_jar_dir):
                print('翻译结果不存在：%s' % translation_jar_dir)
                continue

            for root, dirs, files in os.walk(translation_jar_dir):
                relative_dir = root.replace(translation_jar_dir, '')
                """相对于 jar 文件的目录"""
                if jar_file.endswith('resources_en.jar'):
                    # 解压整个文件夹，以查看是否有新增的文件
                    print('文件夹%s' % root + os.path.sep)
                    for directory in dirs:
                        TranslationFile.unpack_directory_from_jar(jar_file_path,
                                                                  relative_dir + os.path.sep + directory + os.path.sep,
                                                                  output_dir + os.path.sep + jar_file)
                else:
                    # 解压对应文件
                    for file in files:
                        print('文件%s' % root + os.path.sep + file)
                        TranslationFile.unpack_file_from_jar(jar_file_path, relative_dir + os.path.sep + file,
                                                             output_dir + os.path.sep + jar_file)

    @staticmethod
    def unpack_file_from_jar(jar_file, member, path):
        """
        解压 jar 中的一个文件
        """
        # zip 中使用的是 /，不以其开头
        member = member.replace('\\', '/').lstrip('/')
        print('解压 %s 的 %s \n解到 %s' % (jar_file, member, path))
        with zipfile.ZipFile(jar_file) as zip_file:
            zip_file.extract(member, path)

    @staticmethod
    def unpack_directory_from_jar(jar_file, member, path):
        """
        解压 jar 中的一个目录
        """
        # zip 中使用的是 /，不以其开头
        member = member.replace('\\', '/').lstrip('/')
        print('解压 %s 的 %s \n解到 %s' % (jar_file, member, path))
        with zipfile.ZipFile(jar_file) as zip_file:
            for file in zip_file.namelist():
                if file.startswith(member):
                    zip_file.extract(file, path)


if __name__ == '__main__':
    TranslationFile().main()
