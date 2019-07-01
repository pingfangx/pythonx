import os
import shutil
import time
from typing import List, Dict

import xmind
from xmind.core.topic import TopicElement

from xx import filex
from xx import iox


class TopicDir:
    def __init__(self, topic: TopicElement, path: str):
        self.topic = topic
        self.path = path


class XMindUtils:
    def __init__(self, xmind_file_path, root_dir, back_dir):
        self.xmind_file_path = xmind_file_path
        """ xmind 文件"""

        self.root_dir = root_dir
        """根目录"""

        self.back_dir = back_dir
        """备份文件目录"""

    def main(self):
        action_list = [
            ['退出', exit],
            ['显示为 json', self.print_as_json],
            ['根据 xmind 创建目录', self.create_dirs_by_xmind],
            ['根据 xmind 更新目录', self.update_dirs_by_xmind],
        ]
        iox.choose_action(action_list)

    def print_as_json(self):
        workbook = xmind.load(self.xmind_file_path)
        print(workbook.to_prettify_json())

    def update_dirs_by_xmind(self):
        """更新目录"""
        files = filex.list_file(self.back_dir)
        if not files:
            print(f'没有找到备份数据')
            return
        back_file = sorted(files)[-1]
        print(f'选择备份文件 {back_file}')
        origin_dirs = self.collect_xmind_topics(back_file)
        print(f'原始目录')
        print(origin_dirs)

        new_dirs = self.collect_xmind_topics(self.xmind_file_path)
        print(f'新建目录')
        print(new_dirs)

        print()
        print('检查是否需要移动目录')
        origin_dirs_dict = self.dirs_to_dict(origin_dirs)
        new_dirs_dict = self.dirs_to_dict(new_dirs)

        for k, v in origin_dirs_dict.items():
            if k in new_dirs_dict:
                new_v = new_dirs_dict[k]
                if v.path != new_v.path:
                    print(f'目录变化 {v.path} -> {new_v.path}')
                    if os.path.exists(v.path):
                        if not os.path.exists(new_v.path):
                            print(f'目录移动 {v.path} -> {new_v.path}')
                            shutil.move(v.path, new_v.path)
                        else:
                            print(f'目标目录已存在 {new_v.path}')
                            os.rmdir(v.path)
                    else:
                        print(f'源目录已不存在 {v.path}')
            else:
                # 不存在
                try:
                    os.rmdir(v.path)
                except OSError as e:
                    print(f'移除目录出错 {v.path}')
                    print(e)

        print()
        print('检查并创建目录')
        self.create_dirs(new_dirs, False)
        self.back_file()

    def create_dirs_by_xmind(self):
        """根据 xmind 文件创建目录"""
        dirs = self.collect_xmind_topics(self.xmind_file_path)
        self.create_dirs(dirs, True)
        self.back_file()

    def back_file(self):
        """备份文件

        备份文件，根据主题 id，以后有变动时，目录也可以执行变化
        """
        src = self.xmind_file_path
        name, ext = os.path.splitext(os.path.basename(src))
        time_str = time.strftime('%Y%m%d_%H%M%S')

        dir_path = os.path.abspath('ignore')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        dst = os.path.join(dir_path, f'{name}_back_{time_str}{ext}')
        print(f'备份文件 {src} -> {dst}')
        shutil.copy(src, dst)

    def create_dirs(self, dirs: List[TopicDir], verbose=False):
        """创建目录"""
        size = len(dirs)
        print(f'创建共 {size} 个目录')
        for i, topic_dir in enumerate(dirs):
            if verbose:
                print(f'创建 {i + 1}/{size} :{topic_dir.path}')
            self.create_dir(topic_dir.path, verbose)

    @staticmethod
    def create_dir(path, verbose=False):
        """创建目录"""
        if os.path.exists(path):
            if verbose:
                print(f'文件夹已存在')
        else:
            os.makedirs(path)
            if os.path.exists(path):
                print('创建成功')
            else:
                print(f'创建失败')

    @staticmethod
    def dirs_to_dict(dirs: List[TopicDir]) -> Dict[str, TopicDir]:
        return {topicDir.topic.getID(): topicDir for topicDir in dirs}

    def collect_xmind_topics(self, xmind_file) -> List[TopicDir]:
        """根据 xmind 文件收集主题目录"""
        workbook = xmind.load(xmind_file)
        sheet = workbook.getPrimarySheet()
        topic = sheet.getRootTopic()
        return self.collect_topic_to_dirs(topic, self.root_dir)

    def collect_topic_to_dirs(self, topic: TopicElement, parent_dir) -> List[TopicDir]:
        """将主题收集为目录名"""
        current_dir = os.path.join(parent_dir, topic.getTitle())
        dirs = [TopicDir(topic, current_dir)]
        for topic in topic.getSubTopics():
            dirs.extend(self.collect_topic_to_dirs(topic, current_dir))
        return dirs


if __name__ == '__main__':
    XMindUtils(
        xmind_file_path=r'D:\workspace\WorkspaceX\file\mind\知识体系.xmind',
        root_dir=r'D:\workspace\BlogX\xmind',
        back_dir='ignore'
    ).main()
