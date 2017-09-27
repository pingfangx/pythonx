import os
from subprocess import call
from xml.etree import ElementTree as Et

from xx import filex
from xx import iox


class AndroidSourceDownloader:
    """
    参考:Jeanboydev.《 Windows 环境下载 Android 源码》.http://blog.csdn.net/freekiteyu/article/details/70939672
    感谢
    """

    def __init__(self, root_dir, tag, git_path, use_tsinghua=True):
        """
        :param root_dir:根目录 
        :param tag: 要下载的分枝标签
        :param git_path: git路径，如果配置了环境变量，可以直接使用 git
        :param use_tsinghua: 是否使用清华的镜像
        """
        self.root_dir = root_dir
        self.manifest_dir = self.root_dir + os.path.sep + 'manifest'
        self.manifest_file = self.manifest_dir + os.path.sep + 'default.xml'
        self.tag = tag
        self.source_root = self.root_dir + os.path.sep + tag
        self.git_path = git_path
        if use_tsinghua:
            self.project_root = 'https://aosp.tuna.tsinghua.edu.cn'
        else:
            self.project_root = 'https://android.googlesource.com'

    def main(self):
        action_list = [
            ['退出', exit],
            ['clone manifest', self.download_manifest],
            ['clone manifest 并显示所有分枝', self.download_manifest, True],
            ['clone manifest 并切换分枝为 ' + self.tag, self.download_manifest, False, True],
            ['导出下载安卓源码的 cmd.bat', self.download_android_source, self.root_dir + '/cmd.bat'],
            ['下载安卓源码', self.download_android_source],
        ]
        iox.choose_action(action_list)

    def download_manifest(self, show_branch=False, chekcout=False):
        """下载manifest"""
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        os.chdir(self.root_dir)

        if not os.path.exists(self.manifest_dir):
            cmd = '%s clone %s/%s.git' % (self.git_path, self.project_root, 'platform/manifest')
            self.run_cmd(cmd)
        os.chdir(self.manifest_dir)
        if show_branch:
            self.run_cmd('%s branch -a' % self.git_path)
        if chekcout:
            cmd = '%s checkout %s' % (self.git_path, self.tag)
            self.run_cmd(cmd)

    @staticmethod
    def run_cmd(cmd):
        print(cmd)
        call(cmd)

    def download_android_source(self, out_file=None):
        """
        下载安卓源码 
        :param out_file: 输出文件，如果直接运行，不会显示 clone 的进度（可能是我不会，我简单搜了一下，没找到）
        所以先输出为bat文件，再执行
        :return: 
        """
        if not os.path.exists(self.source_root):
            os.mkdir(self.source_root)

        root = Et.parse(self.manifest_file)
        project_list = root.findall('project')
        length = len(project_list)
        result = list()
        for i in range(length):
            project = project_list[i]
            dir_path = project.attrib['path']
            last = dir_path.rfind("/")
            if last != -1:
                # 最后一个名字由 git 创建，将其截去
                dir_path = self.source_root + os.path.sep + dir_path[:last]
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                work_dir = dir_path
            else:
                # 如果没有/，则是在当前目录
                work_dir = self.source_root

            # 执行命令
            name = project.attrib['name']
            cmd = '%s clone %s/%s.git' % (self.git_path, self.project_root, name)
            if out_file:
                result.append('echo %d/%d' % (i + 1, length))
                result.append('cd /d %s' % work_dir)
                result.append(cmd)
            else:
                print('clone %d/%d' % (i + 1, length))
                os.chdir(work_dir)
                self.run_cmd(cmd)
        if out_file:
            filex.write_lines(out_file, result, add_line_separator=True)


if __name__ == '__main__':
    AndroidSourceDownloader(root_dir=r'E:\android', tag='android-7.1.2_r33', git_path='git').main()
