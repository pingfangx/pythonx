import os
import re

from xx import filex
from xx import iox


class FileUtils:
    """文件工具"""

    def main(self):
        action_list = [
            ['退出', exit],
            ['重命名文件索引', self.rename_file_index, r''],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def rename_file_index(dir_path):
        """重命名文件索引"""
        files = filex.list_file(dir_path)
        if not files:
            print('文件为空')
            return

        print(f'1 读取序号模式')
        index_pattern = FileUtils.get_file_index_pattern(files)
        print(f'读取到序号正则为 {index_pattern}')

        print()
        print(f'2 取最长序号')
        max_index = FileUtils.get_max_length_index(files, index_pattern)
        print(f'最长序号为 {max_index},取最大长度为 {len(max_index)}')

        print()
        print(f'3 尝试重命名')
        FileUtils.rename_file_by_max_length_index(files, index_pattern, len(max_index))

        print(f'重命名完成')

    @staticmethod
    def get_file_index_pattern(files):
        """读取文件索引的模式"""
        file = files[0]
        name = os.path.basename(file)
        print(f'首个文件名为 {name}')
        match = re.search(r'([^\d])(\d+)([^\d])', name)
        if not match:
            print(f'未找到序号')
            return
        print(f'找到序号:{match.group()}')
        start, index, end = match.groups()
        print(f'认为序号以【{start}】开头，以【{end}】结尾')
        return re.compile(f'(?<={start})(\\d+)(?={end})')

    @staticmethod
    def get_max_length_index(files, index_pattern) -> str:
        """读取最大长度的序号

        :param files: 文件
        :param index_pattern: 序号正则
        :return:字符串，只判断长度，不作转换
        """
        """"""
        max_index = ''
        for file in files:
            match = re.search(index_pattern, file)
            if not match:
                print(f'文件未找到序号 {index_pattern},{file}')
                return ''
            match_index = match.group()
            if len(max_index) < len(match_index):
                max_index = match_index
        return max_index

    @staticmethod
    def rename_file_by_max_length_index(files, index_pattern, max_length: int):
        """根据最大度的序号命合各文件序号"""
        for file in files:
            # 使用 zfill 补 0
            new_file = re.sub(index_pattern, lambda match: match.group().zfill(max_length), file)
            if file == new_file:
                print(f'无需重命名 {file}')
            else:
                print(f'尝试重命名 {file} -> {new_file}')
                os.rename(file, new_file)


if __name__ == '__main__':
    FileUtils().main()
