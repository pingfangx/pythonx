import hashlib
import os
import queue
import re

import tinify

from xx import iox, filex, threadx


class TinyPng:
    def __init__(self, api_key, source_dir, target_dir=None, minimum_size=1024, keep_files=None, offset=0):
        """

        :param api_key: api key
        :param source_dir: 源目录
        :param target_dir: 目标目录，如果为空，则与源目录相同
        :param minimum_size: 最小文件大小，小于此大小的文件不压缩
        :param keep_files:保留的文件名，可以使胙用正则匹配
        :param offset:全部压缩时的偏移
        """
        tinify.key = api_key
        self.source_dir = source_dir
        self.target_dir = target_dir
        if not self.target_dir:
            self.target_dir = self.source_dir
        self.minimum_size = minimum_size
        self.keep_files = keep_files
        self.offset = offset

    def main(self):
        action_list = [
            ['退出', exit],
            ['校验 API_KEY', self.validate_key],
            ['列出文件', self.list_and_print_file],
            ['压缩第一张', self.compress_first_file],
            ['循环压缩全部', self.compress_all_file_in_loop],
            ['多线程压缩全部', self.compress_all_file_in_thread],
            ['检查压缩结果', self.check_compress_result],
            ['检查相同文件', self.check_same_file],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def validate_key():
        try:
            tinify.validate()
            print(f'校验成功')
            print(f'本月已压缩 {tinify.compression_count} 张')
        except tinify.Error as e:
            print('校验失败')
            print(e)

    def list_and_print_file(self):
        files = self.list_file()
        length = len(files)
        for i in range(self.offset, length):
            file = files[i]
            print(f'{i+1}/{length} {filex.get_file_size_str(file)} {file}')

    def check_compress_result(self):
        files = self.list_file(False)
        self.check_files(files)

    def check_same_file(self):
        files = self.list_file(False)
        md5_list = {}
        for file in files:
            md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
            if md5 in md5_list.keys():
                print(f'{file} 与 {md5_list[md5]} md5 相同，文件大小为 {filex.get_file_size_str(file)}')
            else:
                md5_list[md5] = file

    def list_file(self, ignore_compressed=True):
        # jpg 或 png，但不包括 .9.png
        files = filex.list_file(self.source_dir, '(jpg)|((?<!\.9\.)png)$')
        print(f'过滤掉非图片文件，还剩 {len(files)} 个')

        files = list(filter(self.not_in_keep_files, files))
        print(f'过滤掉保留的文件，还剩 {len(files)} 个')

        files = list(filter(lambda x: os.path.getsize(x) >= self.minimum_size, files))
        print(f'过滤掉小于 {self.minimum_size} 的文件，还剩 {len(files)} 个')

        if ignore_compressed:
            files = list(filter(self.not_compress_yet, files))
            print(f'过滤掉已压缩的文件，还剩 {len(files)} 个')

        return files

    def check_files(self, files):
        """检查文件"""
        length = len(files)
        for i in range(self.offset, length):
            file = files[i]
            source_file_length = os.path.getsize(file)
            target_file_length = os.path.getsize(self.get_target_file(file))

            source_size = filex.parse_file_size(source_file_length)
            target_size = filex.parse_file_size(target_file_length)
            reduce_size = filex.parse_file_size(source_file_length - target_file_length)
            print(f'{i+1}/{length} {source_size} -> {target_size},减小 {reduce_size}, {file}')

    def not_in_keep_files(self, file):
        """不是保留的文件"""
        if self.keep_files:
            for keep_file in self.keep_files:
                file_name = os.path.basename(file)
                file_name = os.path.splitext(file_name)[0]
                if re.fullmatch(keep_file, file_name):
                    return False
        return True

    def not_compress_yet(self, file):
        """尚未压缩"""
        return not os.path.exists(self.get_target_file(file))

    def get_target_file(self, source_file):
        return source_file.replace(self.source_dir, self.target_dir)

    def compress_first_file(self):
        files = self.list_file()
        self.compress_image(files[0])

    def compress_all_file_in_loop(self):
        files = self.list_file()
        length = len(files)
        for i in range(self.offset, length):
            print(f'压缩每 {i+1}/{length} 张图片')
            self.compress_image(files[i])

    def compress_all_file_in_thread(self):
        files = self.list_file()
        length = len(files)

        q = queue.Queue()
        for i in range(self.offset, length):
            q.put(files[i])
        threadx.HandleQueueMultiThread(
            q=q,
            callback=self.compress_image_in_thread,
            thread_num=100,
            print_before_task=True
        ).start()

    def compress_image_in_thread(self, element, element_index, thread_id):
        self.compress_image(element)

    def compress_image(self, source_file):
        target_file = source_file.replace(self.source_dir, self.target_dir)
        # 创建目录
        filex.check_and_create_dir(target_file)

        print(f'开始压缩 {source_file}->{target_file}')
        source = tinify.from_file(source_file)
        try:
            source.to_file(target_file)
        except tinify.errors.AccountError:
            print('压缩数量已超限')
            exit()

        source_length = filex.get_file_size_str(source_file)
        target_length = filex.get_file_size_str(target_file)
        print(f'压缩完成 {source_length}->{target_length}')
        print(f'本月已压缩 {tinify.compression_count} 张')
        if tinify.compression_count >= 500:
            print('压缩数量已超限')
            exit()


if __name__ == '__main__':
    TinyPng('',
            source_dir=r'',
            target_dir=r'',
            minimum_size=1024,
            keep_files=None,
            offset=0).main()
