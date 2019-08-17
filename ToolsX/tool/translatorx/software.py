import functools
import os
import re


class Software:
    """翻译软件"""
    DEFAULT_LOCALE = 'zh_CN'
    """默认区域"""

    def __init__(self,
                 name='',
                 version='',
                 release_version='',
                 software_home_path='',
                 omegat_workspace='',
                 translation_locale=''):
        self.name = name
        """软件名"""

        self.version = version
        """版本"""

        self.locale = translation_locale
        """区域"""

        self.home_path = self.find_home_path(software_home_path)
        """软件安装目录"""

        self.checked = False
        """是否选中，选中才能执行相关操作"""
        if self.home_path:
            self.checked = True

        self.original_jar_list = [
            os.path.join(self.home_path, 'lib', 'resources_en.jar'),
            os.path.join(self.home_path, 'plugins', 'java', 'lib', 'resources_en.jar'),
        ]
        """原始 jar 文件列表
        
        更新 IDEA 2019.2 后，有部分资源移到了 \plugins\java\lib\resources_en.jar
        """

        self.omegat_workspace = omegat_workspace
        """OmegaT 工作目录"""

        self.translation_jar_name = f'resources_{self.locale}_{self.name}_{version}_r{release_version}.jar'
        """输出汉化包的文件名"""

        self.translation_jar_path = os.path.join(self.omegat_workspace, 'jars', self.name, self.translation_jar_name)
        """输出汉化包的目录"""

        self.omegat_workspace_source_software = os.path.join(self.omegat_workspace, 'source', self.name)
        """OmegaT source 目录"""

        self.omegat_workspace_target_software = os.path.join(self.omegat_workspace, 'target', self.name)
        """OmegaT target 目录"""

        self.omegat_workspace_source_resources_en = os.path.join(self.omegat_workspace_source_software, 'resources_en')
        """source 中的软件名下的 resources_en"""

        self.omegat_workspace_target_resources_en = os.path.join(self.omegat_workspace_target_software, 'resources_en')
        """target 中软件名下的 resources_en"""

        self.ignore_file_pattern = self.get_ignore_file_pattern()
        """
        忽略文件的正则
        其中 inspectionDescriptions 和 intentionDescriptions ，以及 InspectionGadgetsBundle.properties 是可以汉化的，只是太多了
        剩余的目录 fileTemplates，META 和 search 是不用翻译的
        """

    def get_check_status(self):
        """输出选中状态"""
        home = self.home_path
        if not home:
            self.checked = False
            home = '(未找到安装路径)'
        return f'{"√" if self.checked else "×"}\t{self.name:20}\t{self.translation_jar_name:50}\t{home}'

    def find_home_path(self, path: str):
        home_path = path
        if self.is_idea_home_path(home_path):
            # 当前配置的就是安装路径
            return home_path

        # 添加上软件名字
        home_path = os.path.join(path, self.name)
        if self.is_idea_home_path(home_path):
            return home_path

        # 检查 Toolbox 的 apps 目录
        apps_path = os.path.join(path, 'apps')
        home_path = self.find_software_home_path_in_toolbox(apps_path, self.name)
        return home_path

    def find_software_home_path_in_toolbox(self, root, software_name):
        """在 toolbox 的安装目录内找出软件目录"""

        if not os.path.isdir(root):
            return ''

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
            if os.path.isdir(os.path.join(software_dir, file)) \
                    and not file.endswith('.plugins'):
                dir_list.append(file)
        if not dir_list:
            return ''
        # 按版本号排序
        dir_list = sorted(dir_list, key=functools.cmp_to_key(self._compare_version), reverse=True)
        software_dir = os.path.join(software_dir, dir_list[0])

        if self.is_idea_home_path(software_dir):
            return software_dir
        else:
            return ''

    @staticmethod
    def get_software_name_in_toolbox(name: str):
        """获取在 toolbox 中的名字，"""
        index = name.upper().find('IDEA')
        if index != -1:
            # 截去前面的 IntelliJ
            return name[index:]
        return name

    def get_execute_file_name(self):
        """获取执行文件的名称"""
        bin_name = self.name
        bin_name = bin_name.split('-')[0]
        if bin_name.lower() == 'AndroidStudio'.lower():
            bin_name = 'Studio'
        elif bin_name.lower() == 'IntelliJIDEA'.lower():
            bin_name = 'idea'
        return f'{bin_name}64.exe'

    @staticmethod
    def _compare_version(x: str, y: str) -> int:
        """比较版本号"""
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

    @staticmethod
    def is_idea_home_path(path):
        """是否是 home 路径

        判断方法来知 idea 源码
        com.intellij.openapi.application.PathManager#isIdeaHome
        """
        return os.path.isfile(os.path.join(path, 'bin', 'idea.properties'))

    def toggle_checked(self):
        """切换选中"""
        if self.checked:
            self.checked = False
        else:
            if self.home_path:  # 有安装路径才能选中
                self.checked = True

    @staticmethod
    def get_ignore_file_pattern():
        """忽略文件的正则

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
        # AndroidStudio tips 中的 excluded 好像也被排除了，翻译没用（如果要翻译，OmegaT 中判断是否是 tips 也要修改）
        ignore_pattern = '^(fileTemplates|inspectionDescriptions|intentionDescriptions|META-INF|search|tips/excluded)'
        # 或者以这几个类型为扩展名的
        ignore_pattern += r'|\.(png|gif|css)$'
        ignore_pattern += r'|(missing_images|icon-robots)\.txt$'
        # 这几个文件太长了，可以以后翻译
        # 这里要加上以 \ 开头，同时要避免被 python 转义，所以写为 \\\\ 或加上 r
        # 后来改为 / ，因为在 zip 中是 /
        ignore_pattern += r'|(\\|/)(InspectionGadgets|IntentionPowerPack|OC|Py|R)Bundle\.properties$'
        # 这是根目录的文件，可以以后翻译
        # ignore_pattern += '|^(CidrDebuggerBundle|RuntimeBundle)\.properties$'
        return re.compile(ignore_pattern)

    def get_file_zip_name(self, name: str) -> str:
        """获取文件压缩进压缩包时的名字

        包括属性文件、tips 文件夹，都是生成的默认的区域，如果设置了，则进行替换
        """
        if self.locale == Software.DEFAULT_LOCALE:  # 默认不需要替换
            return name
        else:  # 直接替换，无须别的处理
            return name.replace(Software.DEFAULT_LOCALE, self.locale)
