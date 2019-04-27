import os
import shutil
import time

from scrapy_spider.scrapy_spider.common.statistic.base_statistics import BaseStatistics
from xx import filex
from xx import iox


class FileUtils:
    """文件工具"""

    def main(self):
        src_dir = [
            r'',
        ]
        dst_dir = r''
        action_list = [
            ['退出', exit],
            ['复制文件到 sd 卡', self.copy_file_to_sdcard, src_dir, dst_dir],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def copy_file_to_sdcard(src_dir, dst_dir):
        """复制文件到内存卡

        该需求是因为部分设备读取内存卡不是按照文件名顺序
        可能是按照存储顺序？
        于是格式化内存卡，然后按顺序指定多个目录，复制进内存卡
        """
        files = []
        is_list = False
        if isinstance(src_dir, list):
            is_list = True
            for path in src_dir:
                files.extend(filex.list_file(path))
        else:
            files.extend(filex.list_file(src_dir))
        length = len(files)
        print(f'共 {length} 个文件')
        if length == 0:
            return
        print(f'读取文件大小')
        sum_size = 0
        for i, file in enumerate(files):
            size = os.path.getsize(file)
            sum_size += size
            print(f'{i + 1}/{length},{file} {filex.parse_file_size(size)}')
        print(f'文件总大小 {filex.parse_file_size(sum_size)}')

        print()
        print(f'开始复制文件')
        copy_size = 0
        start_time = time.time()
        for i, file in enumerate(files):
            if is_list:
                # 如果是多个目录，取目录名
                dir_name = os.path.dirname(file)
                dst_file = os.path.join(dst_dir, os.path.basename(dir_name), os.path.basename(file))
            else:
                # 如果是单个目录，直接取相对路径
                src_file = os.path.relpath(file, src_dir)
                dst_file = os.path.join(dst_dir, src_file)
            print(f'复制文件 {i + 1}/{length},{filex.get_file_size_str(file)},{file} -> {dst_file}')
            # 复制文件
            filex.check_and_create_dir(dst_file)
            shutil.copyfile(file, dst_file)
            # 因为太大，需要记录进度
            copy_size += os.path.getsize(file)
            print(f'已复制 {filex.parse_file_size(copy_size)}/{filex.parse_file_size(sum_size)}')
            # 记录时间
            FileUtils.count_time(start_time, copy_size / 1024 / 1024, sum_size / 1024 / 1024, 'M')

    @staticmethod
    def count_time(start_time, count, total, name='items'):
        """计时"""
        spend_time = time.time() - start_time
        if spend_time == 0:
            spend_time = 1
        speed = count / spend_time
        remaining_time = (total - count) / speed
        print(f'{count}/{total} {name}, took {FileUtils.format_time(spend_time)},'
              f' speed {speed * 60:.2f} {name}/min,'
              f' remains {FileUtils.format_time(remaining_time)}')

    @staticmethod
    def format_time(second):
        """格式化时间"""
        return BaseStatistics.format_time(second)


if __name__ == '__main__':
    FileUtils().main()
