import filecmp
import functools
import os
import re
import shutil
import zipfile

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from tool.android.android_studio_translator import Tips
from tool.android.android_studio_translator.tools import Tools
from tool.android.android_studio_translator.translator.translation_file import TranslationFile
from xx import filex
from xx import iox


class JetBrainsTranslator:
    """汉化多个软件"""

    def __init__(self):
        self.work_dir = r'D:\workspace\TranslatorX\JetBrains'
        self.source_dir = self.work_dir + os.path.sep + 'source'
        self.target_dir = self.work_dir + os.path.sep + 'target'

        current_version_list = [
            '3.3',
            '2018.3',
        ]

        pre_version_list = [
            '3.0.1',
            '2017.3.1',
        ]
        "不再维护上一个版本，除比较 jar 包，比较 build 判断是否更新，等方法用到以外，主要的方法都不再用到"

        software_name_list = [
            'AndroidStudio',
            # 'CLion',
            # 'GoLand',
            # 'IntelliJIDEA',
            # 'PhpStorm',
            # 'PyCharm',
            # 'RubyMine',
            # 'WebStorm',
        ]

        software_root_dir = r'D:/software/JetBrains/'
        self.software_list = []
        for i in range(len(software_name_list)):
            software_name = software_name_list[i]
            if i >= len(current_version_list):
                # 取最后一个
                version = current_version_list[-1]
            else:
                # 取对应版本
                version = current_version_list[i]
            if '-' in version:
                version, release_version = version.split('-')
            else:
                release_version = 1

            if i >= len(pre_version_list):
                pre_version = pre_version_list[-1]
            else:
                pre_version = pre_version_list[i]
            if '-' in pre_version:
                pre_version, pre_release_version = pre_version.split('-')
            else:
                pre_release_version = 1
            software_path = self.find_software_path(software_root_dir, software_name)
            software = Software(self.work_dir, software_path, software_name, version, pre_version,
                                release_version, pre_release_version)
            self.software_list.append(software)

    def main(self):
        action_list = [
            ['退出', exit],
            ['-tips 相关的', ],
            ['解压出清单文件', self.iter_software, lambda x: x.extra_tips_manifest_file()],
            ['处理清单文件，整理tips的名称方便翻译', self.iter_software, lambda x: x.process_tips_manifest_file()],
            ['检查并补全缺少的tips名', self.iter_software, lambda x: x.check_and_append_tips_name()],
            ['将 tips 翻译结果的unicode转为中文', self.iter_software, lambda x: x.change_unicode_to_chinese()],

            ['-翻译前应该处理的', ],
            ['检查官网是否有新版本', self.check_update],
            ['复制 resources_en.jar', self.iter_software, lambda x: x.copy_resources_en_jar()],
            ['解压 jar 到 source 目录', self.iter_software, lambda x: x.extract_jar_to_source_dir()],

            ['-翻译后应该处理的', ],
            ['将 tips 翻译结果的unicode转为中文', self.iter_software, lambda x: x.change_unicode_to_chinese()],
            ['处理tips翻译结果为AndroidStudio用', self.iter_software, lambda x: x.process_tips_translation_result()],
            ['压缩进汉化包(处理 tips)', self.iter_software, lambda x: x.zip_translation(rename_tips=True)],
            ['压缩进汉化包', self.iter_software, lambda x: x.zip_translation()],
            ['压缩进 en 包', self.iter_software, lambda x: x.zip_translation_to_en()],

            ['-以下是工具的方法', ],
            ['将汉化包复制到软件目录', self.iter_software, lambda x: x.copy_translation_to_work_dir(1)],
            ['将 en 汉化包复制到软件目录', self.iter_software, lambda x: x.copy_translation_to_work_dir(2)],
            ['将英文包复制到软件目录', self.iter_software, lambda x: x.copy_translation_to_work_dir(3)],
            ['向启动文件写入 crack 配置', self.iter_software, lambda x: x.write_crack_config()],
            ['输出版本号', self.iter_software_without_print, lambda x: x.print_software_version()],
            ['输出版本号及汉化包版本号', self.iter_software_without_print, lambda x: x.print_software_version(True)],
            ['输出下载地址', self.iter_software_without_print, lambda x: x.print_software_download_url()],

            ['-弃用的', ],
            ['重命名_zh_CN', self.rename_cn_files],
            ['校验版本是否更新', self.iter_software, lambda x: x.validate_version()],
            ['检查 jar 包是否变化', self.iter_software, lambda x: x.compare_jar()],
            ['删除比较 jar 包时的缓存', self.iter_software, lambda x: x.delete_compare_tmp_dir()],
        ]
        iox.choose_action(action_list)

    def rename_cn_files(self):
        project_name_list = os.listdir(self.source_dir)
        for project_name in project_name_list:
            project_path = self.target_dir + os.sep + project_name
            if os.path.isdir(project_path):
                project_messages_path = project_path + os.sep + 'resources_en' + os.sep + 'messages'
                TranslationFile.rename_cn_files(project_messages_path)

    def iter_software_without_print(self, callback):
        self.iter_software(callback, False)

    def iter_software(self, callback, print_msg=True):
        """对所有软件循环进行操作"""
        length = len(self.software_list)
        for i in range(length):
            software = self.software_list[i]
            if print_msg:
                print('\n处理%d/%d %s %s ' % (i + 1, length, software.name, software.version))
            callback(software)

    def check_update(self, chrome_path=None):
        """检查更新"""
        print('启动 chrome')
        chrome_options = None
        if chrome_path:
            chrome_options = ChromeOptions()
            chrome_options.binary_location = chrome_path
        driver = webdriver.Chrome(chrome_options=chrome_options)
        self.check_update_android_studio(driver)
        self.check_update_from_official_website(driver)
        driver.quit()

    def check_update_android_studio(self, driver=None):
        """检查 Android Studio 更新"""
        for software in self.software_list:
            name, version = software.name, software.version
            if name == 'AndroidStudio':
                print(name, version)
                url = 'https://developer.android.google.cn/studio/index.html'
                print('open %s' % url)
                if not driver:
                    driver = webdriver.Chrome()
                driver.get(url)
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                latest_version = soup.select_one('div.dac-studio-version').text
                latest_version = latest_version.split('for')[0].strip()
                if version == latest_version:
                    print('%s 已经是最新版本 %s' % (name, version))
                else:
                    print('%s 的最新版本为 %s ，当前版本为 %s' % (name, latest_version, version))
                break

    def check_update_from_official_website(self, driver=None, retry_times=0):
        """从 JetBrains 官网检查是否有更新"""
        url = 'https://www.jetbrains.com/products.html'
        print('打开 %s' % url)
        if not driver:
            driver = webdriver.Chrome()
        driver.get(url)
        # print('开始解析')
        # 解析结果
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products_group = soup.select_one('.g-row.products-list.js-products-list')
        if products_group is None:
            if retry_times <= 10:
                retry_times += 1
                print('没有正确的产品列表，第 %d 次重试' % retry_times)
                self.check_update_from_official_website(driver, retry_times)
            else:
                print('重试超过 10 次，失败')
            return
        product_div_list = products_group.select('div.g-col-4')
        latest_version = {}
        for product_div in product_div_list:
            title = product_div.select_one('.product-item__title')
            if title:
                title = title.text.strip()
            version = product_div.select_one('.product-item__version')
            if version:
                version = version.text.strip()
            if title and version:
                latest_version[title] = version
        print('解析出所有软件为')
        print(latest_version)
        version_result = ''
        for software in self.software_list:
            name, version = software.name, software.version
            name = name.replace('IntelliJIDEA', 'IntelliJ IDEA')
            if name in latest_version.keys():
                version_result += "\n'%s'," % latest_version[name]
                if version == latest_version[name]:
                    print('%s 已经是最新版本 %s' % (name, version))
                else:
                    print('%s 的最新版本为 %s ，当前版本为 %s' % (name, latest_version[name], version))
            else:
                print('没有找到软件名 %s' % name)
        print(version_result)

    def find_software_path(self, software_root_dir, software_name):
        """查找软件的安装路径"""
        # 是否安装在对应文件夹
        path = os.path.join(software_root_dir, software_name)
        if os.path.exists(path):
            return path
        # 查看 apps 目录（使用 Toolbox 安装的目录）
        path = self.find_software_path_in_toolbox(os.path.join(software_root_dir, 'apps'), software_name)
        if not path:
            print(f'无法在 {software_root_dir} 内找到 {software_name} 的安装目录')
            exit(1)
        return path

    def get_software_name_in_toolbox(self, name: str):
        """获取在 toolbox 中的名字，"""
        if 'IDEA' in name.upper():
            return 'IDEA'
        return name

    def find_software_path_in_toolbox(self, root, software_name):
        """在 toolbox 的安装目录内找出软件目录"""
        # 在 apps 内的多个子目录找出软件的目录
        file_list = os.listdir(root)
        software_name = self.get_software_name_in_toolbox(software_name)
        software_dir = ''
        for file in file_list:
            if os.path.isdir(os.path.join(root, file)) and software_name.lower() in file.lower():
                software_dir = file
        if not software_dir:
            return ''

        software_dir = os.path.join(root, software_dir, 'ch-0')
        if not os.path.exists(software_dir):
            return ''

        # ch-0 内可能有多个版本
        file_list = os.listdir(software_dir)
        dir_list = []
        # 列出所有文件夹
        for file in file_list:
            if os.path.isdir(os.path.join(software_dir, file)):
                dir_list.append(file)
        if not dir_list:
            return ''
        # 按版本号排序
        dir_list = sorted(dir_list, key=functools.cmp_to_key(self.compare_version), reverse=True)
        software_dir = os.path.join(software_dir, dir_list[0])
        # 这里还可以校验目录是否正确
        return software_dir

    @staticmethod
    def compare_version(x: str, y: str) -> int:
        list1 = x.split('.')
        list2 = y.split('.')
        if not list1 and not list2:
            return 0
        elif not list1:
            return -1
        elif not list2:
            return 1
        length1 = len(list1)
        length2 = len(list2)
        i = 0
        for i in range(length1):
            if i >= length2:
                # 因为 2 中没有，2 较小
                return 1
            else:
                # 比较
                code1 = 0
                code2 = 0
                try:
                    code1 = int(list1[i])
                except ValueError:
                    pass
                try:
                    code2 = int(list2[i])
                except ValueError:
                    pass
                r = code1 - code2
                if r != 0:
                    return r
        # 循环结束
        if i == length2:
            return 0
        else:
            # 2 还有，1 较小
            return -1


class Software:
    def __init__(self, work_dir, path, name: str = None, version=None, pre_version=None, release_version=1,
                 pre_release_version=-1):
        self.work_dir = work_dir
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
        self.pre_version = pre_version
        "上一个版本"
        if pre_release_version == -1:
            # 没有传参，取默认
            if release_version > 1:
                # -1
                pre_release_version = release_version - 1
            else:
                pre_release_version = 1
        self.release_version = release_version
        "当前软件版本下的汉化包版本，如果需要，可以手动设置，分开设置"
        self.pre_release_version = pre_release_version
        self.en_jar_path = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.version, 'resources_en.jar')
        "软件的英文包"
        self.translation_jar_name = 'resources_zh_CN_%s_%s_r%s.jar' % (self.name, self.version, self.release_version)
        "汉化包文件名"
        self.translation_jar = '%s/jars/%s/%s' % (self.work_dir, self.name, self.translation_jar_name)
        "汉化包完整路径"
        self.translation_en_jar = self.en_jar_path.replace('英文包', '2-替换 lib 中原文件的汉化包')
        """替换原文件的汉化包"""

        """
        现在基本都翻译完了，剩下的是一些硬骨头，不好啃
        2 个文件夹
        inspectionDescriptions 和 intentionDescriptions 
        是检查和意向描述，分别有 1002 个和 212 个文件
        
        5 个 Bundle.properties 文件
        InspectionGadgets，IntentionPowerPack 和 OC 是 AndroidStudio 中的文件
        Py 和 R 分别是 PyCharm 和 RubyMine 中的文件
        条目数分别为
        377
        2226
        208
        689
        1826
        """
        # 以这几个文件夹开头的
        # |com|i18n|org ，可以以后翻译
        ignore_pattern = '^(fileTemplates|inspectionDescriptions|intentionDescriptions|META-INF|search)'
        # 或者以这几个类型为扩展名的
        ignore_pattern += '|\.(png|gif|css)$'
        ignore_pattern += '|(missing_images|icon-robots)\.txt$'
        # 这几个文件太长了，可以以后翻译
        # 这里要加上以 \ 开头，同时要避免被 python 转义，所以写为 \\\\ 或加上 r
        # 后来改为 / ，因为在 zip 中是 /
        ignore_pattern += r'|(\\|/)(InspectionGadgets|IntentionPowerPack|OC|Py|R)Bundle\.properties$'
        # 这是根目录的文件，可以以后翻译
        # ignore_pattern += '|^(CidrDebuggerBundle|RuntimeBundle)\.properties$'
        self.ignore_pattern = re.compile(ignore_pattern)
        """
        忽略文件的正则
        其中 inspectionDescriptions 和 intentionDescriptions ，以及 InspectionGadgetsBundle.properties 是可以汉化的，只是太多了
        剩余的目录 fileTemplates，META 和 search 是不用翻译的
        """

    def copy_resources_en_jar(self):
        """复制 jar"""
        if not os.path.exists(self.path):
            print('软件目录不存在 %s' % self.path)
            return

        build_file_path = self.path + os.sep + 'build.txt'
        if not os.path.exists(build_file_path):
            print('build.txt 不存在')
            return
        destination_build_file_path = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.version, 'build.txt')
        print('复制 %s 到 %s' % (build_file_path, destination_build_file_path))
        filex.check_and_create_dir(destination_build_file_path)
        shutil.copyfile(build_file_path, destination_build_file_path)

        jar_file_path = self.path + os.sep + 'lib' + os.sep + 'resources_en.jar'
        if not os.path.exists(jar_file_path):
            print('jar 包不存在')
            return
        print('复制 %s 到 %s' % (jar_file_path, self.en_jar_path))
        shutil.copyfile(jar_file_path, self.en_jar_path)

    def get_original_en_jar_path(self):
        return self.path + os.sep + 'lib' + os.sep + 'resources_en.jar'

    def zip_translation(self, rename_tips=False):
        """打包翻译"""
        translation_dir = '%s/target/%s/resources_en' % (self.work_dir, self.name)
        print('将 %s 压缩到 %s' % (translation_dir, self.translation_jar))
        source_jar = None
        if not rename_tips or self.name.lower() == 'AndroidStudio'.lower():
            # 重命名 tips 的时候，AndroidStudio 无法读取图片
            source_jar = self.path + os.sep + 'lib' + os.sep + 'resources_en.jar'
        self.zip(translation_dir, self.translation_jar, source_jar, rename_tips=rename_tips)

    def zip_translation_to_en(self):
        """打包翻译到 resource_en 中"""
        translation_dir = '%s/target/%s/resources_en' % (self.work_dir, self.name)
        print('将 %s 压缩到 %s' % (translation_dir, self.translation_en_jar))
        self.zip(translation_dir, self.translation_en_jar, self.en_jar_path, True)

    @staticmethod
    def zip(source_dir, target_jar, source_jar=None, all_file=False, rename_tips=False):
        """
        将 source_jar 的文件压缩进 target_jar
        如果 source_dir 中存在文件，则取 source_dir 中的，不取 source_jar 中的
        :param source_dir: 要压缩的目录
        :param target_jar: 目标 jar
        :param source_jar: 源 jar
        :param all_file: 如果为 false，只压缩 source_dir 对应的文件
        如果为 true ，压缩所有文件
        :param rename_tips: 是否重命名 tips
        :return:
        """
        # 移除 target
        if os.path.exists(target_jar):
            os.remove(target_jar)
        # 创建目录
        filex.check_and_create_dir(target_jar)
        # 写入 source_jar 中的文件
        if source_jar is not None:
            # 记录文件和目录
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
            # 解压仅存在于 source_jar 中，source_dir 中没有的内容
            print('压缩仅在 source_jar 中的文件')
            with zipfile.ZipFile(target_jar, 'a') as target_zip_file:
                with zipfile.ZipFile(source_jar, 'r') as zip_file:
                    for name in zip_file.namelist():
                        need_extract = all_file
                        # 如果是所有文件，那么 source_dir 中不包含的文件夹也要压缩
                        if not need_extract:
                            # 如果不是所有文件，那么只压缩 source_dir 中包含的文件夹
                            for translation_dir in translation_dir_list:
                                if name.startswith(translation_dir):
                                    # 以源目录开头
                                    need_extract = True
                                    break
                        if need_extract:
                            # 需要压缩文件夹，再判断文件是否存在于 source_dir 中，存在则不需要压缩
                            cn_name = '_zh_CN'.join(os.path.splitext(name))
                            if name in translation_file_list or cn_name in translation_file_list:
                                # 存在于中文或英文
                                need_extract = False
                        if need_extract:
                            if all_file:
                                arcname = name.replace('_zh_CN', '')
                            else:
                                arcname = name
                            if rename_tips:
                                arcname = name.replace('tips/', 'tips_zh_CN/')
                            # 写入文件
                            # print('压缩 %s 为 %s' % (name, arcname))
                            with zip_file.open(name) as tmp_file:
                                target_zip_file.writestr(arcname, tmp_file.read())
        # 压缩翻译内容，如果是所有文件，则需要重命名
        ZipTools.zip_jar(source_dir, target_jar, all_file, rename_tips)

    def copy_translation_to_work_dir(self, jar_type=1):
        """
        复制汉化包到工作目录
        :param jar_type: 1 为中文包，2 为 en 中文包，3 为英文包
        :return:
        """

        # 上一版本号
        if jar_type == 1:
            translation_jar_name = self.translation_jar_name
            translation_jar_path = self.translation_jar
        elif jar_type == 2:
            translation_jar_name = 'resources_en.jar'
            translation_jar_path = self.translation_en_jar
        elif jar_type == 3:
            translation_jar_name = 'resources_en.jar'
            translation_jar_path = self.en_jar_path
        else:
            print('类型不正确', jar_type)
            return
        lib_dir = self.path + os.sep + 'lib'
        for file in os.listdir(lib_dir):
            if file.startswith('resources_cn') and file.endswith('.jar'):
                if jar_type != 1 or file != self.translation_jar_name:
                    # 不是中文包，或者不相同删除
                    file_path = lib_dir + os.sep + file
                    try:
                        os.remove(file_path)
                        print('删除', file_path)
                    except PermissionError:
                        print('删除失败', file_path)
        jar_file_path = self.path + os.sep + 'lib' + os.sep + translation_jar_name
        print('复制 %s 到 %s' % (translation_jar_path, jar_file_path))
        shutil.copyfile(translation_jar_path, jar_file_path)

    def validate_version(self):
        """校验是否已更新软件"""

        build_file_path = self.path + os.sep + 'build.txt'
        if not os.path.exists(build_file_path):
            print('build.txt 不存在')
            return

        pre_build_file_path = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.pre_version, 'build.txt')
        if not os.path.exists(pre_build_file_path):
            print('上一版本的 build.txt 不存在')
            return

        print('比较 %s 和 %s' % (build_file_path, pre_build_file_path))
        if filecmp.cmp(build_file_path, pre_build_file_path):
            print('当前版本与前一版本相同，请先更新软件')
            return
        else:
            print('不相同')
            print(filex.read_lines(build_file_path))
            print(filex.read_lines(pre_build_file_path))

    def compare_jar(self):
        """比较 jar 包是否变化"""
        f1 = self.en_jar_path
        f2 = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.pre_version, 'resources_en.jar')
        if not os.path.exists(f1):
            print('不存在 %s' % f1)
        if not os.path.exists(f2):
            print('不存在 %s' % f2)
        print('比较 %s 与 %s' % (f1, f2))
        if filecmp.cmp(f1, f2):
            print('jar 包完全相同')
            return
        print('1-收集要比较的文件夹')
        source_dir = '%s/target/%s/resources_en' % (self.work_dir, self.name)
        translation_dir_list = []
        for root, dirs, files in os.walk(source_dir):
            for dir_name in dirs:
                path = root + '/' + dir_name
                translation_dir_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
        print(translation_dir_list)

        print('2-解压出要比较的文件夹')
        tmp_dir1 = os.path.splitext(f1)[0]
        tmp_dir2 = os.path.splitext(f2)[0]
        ignore_ext = [
            '.png',
            '.gif',
            '.css',
        ]
        with zipfile.ZipFile(f1) as zipfile1:
            with zipfile.ZipFile(f2) as zipfile2:
                namelist1 = zipfile1.namelist()
                namelist2 = zipfile2.namelist()
                for name1 in namelist1:
                    ext = os.path.splitext(name1)[1]
                    if ext in ignore_ext:
                        continue
                    for translation_dir in translation_dir_list:
                        if name1.startswith(translation_dir):
                            # print('比较 %s' % name1)
                            if name1 in namelist2:
                                zipfile1.extract(name1, tmp_dir1)
                                zipfile2.extract(name1, tmp_dir2)
                            else:
                                print('%s 在f1 中有,但 f2 中没有' % name1)
        print('3-比较解压出的文件')
        for root, dirs, files in os.walk(tmp_dir1):
            for file_name in files:
                path1 = root + '/' + file_name
                path2 = path1.replace(tmp_dir1, tmp_dir2)
                if not os.path.exists(path2):
                    print('%s 不存在' % path2)
                    continue
                if not filecmp.cmp(path1, path2):
                    print('不相同 %s 与 %s' % (path1, path2))
                else:
                    # 相同,将文件删除
                    # print('文件相同 %s 与 %s' % (path1, path2))
                    os.remove(path1)
                    os.remove(path2)

    def delete_compare_tmp_dir(self):
        """删除比较时解压的临时文个夹"""
        f1 = self.en_jar_path
        f2 = '%s/jars/%s/英文包/%s/%s' % (self.work_dir, self.name, self.pre_version, 'resources_en.jar')
        tmp_dir1 = os.path.splitext(f1)[0]
        tmp_dir2 = os.path.splitext(f2)[0]
        if os.path.exists(tmp_dir1):
            print('删除 %s' % tmp_dir1)
            shutil.rmtree(tmp_dir1)
        if os.path.exists(tmp_dir2):
            print('删除 %s' % tmp_dir2)
            shutil.rmtree(tmp_dir2)

    def extract_jar_to_source_dir(self):
        """将 jar 解压到 source 目录"""
        out_dir = '%s/source/%s/resources_en' % (self.work_dir, self.name)
        print(f'清空 source 目录 {out_dir}')
        shutil.rmtree(out_dir)
        with zipfile.ZipFile(self.get_original_en_jar_path()) as zip_file:
            namelist = zip_file.namelist()
            for name in namelist:
                if re.search(self.ignore_pattern, name):
                    # print('过滤', name)
                    continue
                print('解压 %s 到 %s' % (name, out_dir))
                zip_file.extract(name, out_dir)

    def write_crack_config(self):
        """向启动配置文件中写入破解 jar 包"""
        name = self.name
        if name == 'IntelliJIDEA':
            name = 'IDEA'
        # config_file = '%s/bin/%s64.exe.vmoptions' % (self.path, name)
        # Toolbox 每个版本的软件是单独的目录，单独的文件，目录名直接拼上扩展名即可
        config_file = f'{self.path}.vmoptions'
        if not os.path.exists(config_file):
            print('配置文件不存在', config_file)
            return
        print(f'配置文件 {config_file}')
        crack_jar_file = r'D:\software\JetBrains\crack\JetbrainsIdesCrack-3.4-release-enc.jar'
        write_line = '-javaagent:%s\n' % crack_jar_file

        with open(config_file, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i]
                if line.startswith('-javaagent'):
                    if crack_jar_file in line:
                        # 已经包含了,不需要设置
                        print('已经包含配置,无需修改')
                    else:
                        # 不包含,修改该行
                        lines[i] = write_line
                        print('修改配置')
                        with open(config_file, 'w') as f2:
                            f2.writelines(lines)
                    return
            # 没有找到行,需要添加
            with open(config_file, 'a') as f2:
                print('添加配置')
                f2.write(write_line)

    activationCode = """
{"licenseId":"ThisCrackLicenseId",
"licenseeName":"pingfangx",
"assigneeName":"pingfangx",
"assigneeEmail":"rover12421@163.com",
"licenseRestriction":"For Rover12421 Crack, Only Test! Please support genuine!!!",
"checkConcurrentUse":false,
"products":[
{"code":"II","paidUpTo":"2099-12-31"},
{"code":"DM","paidUpTo":"2099-12-31"},
{"code":"AC","paidUpTo":"2099-12-31"},
{"code":"RS0","paidUpTo":"2099-12-31"},
{"code":"WS","paidUpTo":"2099-12-31"},
{"code":"DPN","paidUpTo":"2099-12-31"},
{"code":"RC","paidUpTo":"2099-12-31"},
{"code":"PS","paidUpTo":"2099-12-31"},
{"code":"DC","paidUpTo":"2099-12-31"},
{"code":"RM","paidUpTo":"2099-12-31"},
{"code":"CL","paidUpTo":"2099-12-31"},
{"code":"PC","paidUpTo":"2099-12-31"},
{"code":"DB","paidUpTo":"2099-12-31"},
{"code":"GO","paidUpTo":"2099-12-31"},
{"code":"RD","paidUpTo":"2099-12-31"}
],
"hash":"2911276/0",
"gracePeriodDays":7,
"autoProlongated":false}
    """

    def get_tips_manifest_file_path(self):
        """获取 tips 清单文件的目录"""
        return os.path.join(self.work_dir, 'source', self.name, 'IdeTipsAndTricks', 'IdeTipsAndTricks.xml')

    def get_tips_files_dir(self):
        return os.path.join(self.work_dir, 'source', self.name, 'resources_en', 'tips')

    def extra_tips_manifest_file(self):
        """从不同软件的 jar 包中解压出 tips 的清单文件

        Android Studio 和 IntelliJIDEA位于 resources.jar\META-INF\IdeTipsAndTricks.xml
        goland.jar
        phpstorm.jar\META-INF\PhpStormTipsAndTricks.xml
        pycharm.jar
        rubymine.jar
        webstorm.jar
        """

        # jar 包路径
        jar_path = self.path + os.sep + 'lib' + os.sep
        if self.name.lower() in ['AndroidStudio'.lower(), 'IntelliJIDEA'.lower()]:
            jar_path += 'resources'
        else:
            jar_path += self.name
        jar_path += '.jar'

        # 在 jar 包内的路径
        tips_file_in_jar = 'META-INF/'
        if self.name.lower() in [i.lower() for i in ['PhpStorm', 'CLion']]:
            tips_file_in_jar += self.name
        elif self.name.lower() == 'GoLand'.lower():
            tips_file_in_jar += 'Go'
        else:
            tips_file_in_jar += 'Ide'
        tips_file_in_jar += 'TipsAndTricks.xml'
        print(jar_path, tips_file_in_jar)

        if not os.path.exists(jar_path):
            print('jar 包不存在', jar_path)
            return

        tips_manifest_file_path = self.get_tips_manifest_file_path()
        filex.check_and_create_dir(tips_manifest_file_path)
        ZipTools.extra_file(jar_path, tips_file_in_jar, tips_manifest_file_path)

    def process_tips_manifest_file(self):
        """
        处理 tips 的清单文件，由清单文件生成包含清单中所有文件名的待翻译文件
        """
        tips_manifest_file_path = self.get_tips_manifest_file_path()
        if os.path.exists(tips_manifest_file_path):
            print('处理 %s' % tips_manifest_file_path)
            tips = Tips()
            tips_en_file = filex.get_result_file_name(tips_manifest_file_path, '_en', 'properties')
            tips.process_tips_manifest_file(tips_manifest_file_path, tips_en_file)

    def check_and_append_tips_name(self):
        tips_manifest_file_path = self.get_tips_manifest_file_path()
        if os.path.exists(tips_manifest_file_path):
            print('处理 %s' % tips_manifest_file_path)
            tips = Tips()
            tips_files_dir = self.get_tips_files_dir()
            tips_en_file = filex.get_result_file_name(tips_manifest_file_path, '_en', 'properties')
            tips.check_and_append_tips_name(tips_files_dir, tips_en_file, tips_en_file)

    def change_unicode_to_chinese(self):
        tips_manifest_file_dir = os.path.dirname(self.get_tips_manifest_file_path())
        tips_file_path = os.path.join(tips_manifest_file_dir, 'IdeTipsAndTricks_en_zh_CN.properties')
        tips_cn_file_path = os.path.join(tips_manifest_file_dir, 'IdeTipsAndTricks_cn.properties')
        if os.path.exists(tips_file_path):
            print('处理 %s' % tips_file_path)
            Tools.change_unicode_to_chinese(tips_file_path, tips_cn_file_path)

    def process_tips_translation_result(self):
        tips_manifest_file_dir = os.path.dirname(self.get_tips_manifest_file_path())
        tips_cn_file_path = os.path.join(tips_manifest_file_dir, 'IdeTipsAndTricks_cn.properties')
        if os.path.exists(tips_cn_file_path):
            print('处理 %s' % tips_cn_file_path)
            project_tips_path = os.path.join(self.work_dir, 'source', self.name, 'resources_en', 'tips')
            tips = Tips()
            tips.process_tips_translation_result(tips_cn_file_path, project_tips_path,
                                                 Tips.RESULT_TYPE_ANDROID_STUDIO, project_tips_path)

    def print_software_version(self, print_release_version=False):
        """输出版本号"""
        if print_release_version:
            print('%s %s_r%s' % (
                str(self.name).replace('IntelliJIDEA', 'IntelliJ IDEA'), self.version, self.release_version))
        else:
            print('%s %s' % (str(self.name).replace('IntelliJIDEA', 'IntelliJ IDEA'), self.version))

    def print_software_download_url(self):
        software_name = self.name.replace('IntelliJIDEA', 'IntelliJ IDEA')
        print(
            f'## {software_name}\n* {self.version}——{self.translation_jar_name} \n'
            f'[[github](https://github.com/pingfangx/jetbrains-in-chinese/tree/master/{self.name})] \n'
            f'[[百度云]]\n')


class ZipTools:
    @staticmethod
    def zip_jar(source_dir, target_jar, rename_cn=False, rename_tips=False):
        """
        压缩文件夹
        :param source_dir:
        :param target_jar:
        :param rename_cn: 是否将 _zh_CN 重命名再压缩
        :return:
        """
        print('压缩 %s 到 %s' % (source_dir, target_jar))
        filex.check_and_create_dir(target_jar)
        translation_file_list = []
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                path = root + '/' + file_name
                translation_file_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
        with zipfile.ZipFile(target_jar, 'a') as zip_file:
            for file in translation_file_list:
                if rename_cn:
                    arcname = file.replace('_zh_CN', '')
                else:
                    arcname = file
                if rename_tips:
                    arcname = file.replace('tips/', 'tips_zh_CN/')
                # print('压缩 %s 为 %s' % (file, arcname))
                zip_file.write(source_dir + os.sep + file, arcname)

    @staticmethod
    def extra_file(zip_file_path, file_path, output, print_msg=True):
        """解压文件"""
        with zipfile.ZipFile(zip_file_path) as zip_file:
            if file_path not in zip_file.namelist():
                if print_msg:
                    print('文件不存在 jar 包中', file_path)
                return
            if print_msg:
                print('解压 %s!%s 为 %s' % (zip_file_path, file_path, output))
            # zip_file.extract(file_path, output)
            # 这里无法直接导出至指定文件
            with zip_file.open(file_path) as in_file:
                with open(output, 'w') as output_file:
                    output_file.write(in_file.read().decode())


if __name__ == '__main__':
    JetBrainsTranslator().main()
