import hashlib
import os
import queue
import re
import shutil

import tinify

from xx import iox, filex, threadx


class TinyPng:
    def __init__(self, api_key, source_dir, target_dir=None, old_target_dir=None, minimum_size=1024, keep_files=None,
                 offset=0):
        """

        :param api_key: api key
        :param source_dir: 源目录
        :param target_dir: 目标目录，如果为空，则与源目录相同
        :param old_target_dir: 旧版的目标目录
        :param minimum_size: 最小文件大小，小于此大小的文件不压缩
        :param keep_files:保留的文件名，可以使胙用正则匹配
        :param offset:全部压缩时的偏移
        """
        tinify.key = api_key
        self.source_dir = source_dir
        self.target_dir = target_dir
        if not self.target_dir:
            self.target_dir = self.source_dir
        self.old_target_dir = old_target_dir
        self.minimum_size = minimum_size
        self.keep_files = keep_files
        if isinstance(self.keep_files, str):
            # 如果是字符串，认为是文件
            self.keep_files = filex.read_lines(self.keep_files, ignore_line_separator=True)
        self.offset = offset
        self.md5_file = 'ignore/md5.txt'

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
            ['将结果文件复制到源目录', self.copy_target_file_to_source_dir],
            ['-以下用来更新时使用，先切到之前的版本，生成 md5 ，再切回当前版本，复制'],
            ['生成当前所有源文件的 md5', self.generate_md5_of_current_source_files, self.md5_file],
            ['将当前所有源文件复制到目标目录', self.copy_source_file_to_target_dir],
            ['根据文件 md5 复制已压缩文件', self.copy_tiny_png_by_md5, self.md5_file, self.old_target_dir],
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
        files = self.list_need_compress_file()
        length = len(files)
        for i in range(self.offset, length):
            file = files[i]
            print(f'{i + 1}/{length} {filex.get_file_size_str(file)} {file}')

    def check_compress_result(self):
        """检查压缩结果"""
        self.check_files(self.list_source_image_file())

    def check_same_file(self):
        """检查源目录中的相同文件"""
        files = self.list_source_image_file()
        md5_list = {}
        for file in files:
            md5 = self.get_file_md5(file)
            if md5 in md5_list.keys():
                print(f'{file} 与 {md5_list[md5]} md5 相同，文件大小为 {filex.get_file_size_str(file)}')
            else:
                md5_list[md5] = file

    def copy_target_file_to_source_dir(self):
        """
        将结果文件复制到源目录
        """
        self.check_files(self.list_source_image_file(), move=1)

    def copy_source_file_to_target_dir(self):
        """
        将源文件复制到目标目录
        即认为当前源文件的所有文件是压缩后的结果，不再执行压缩
        """
        self.check_files(self.list_source_image_file(), move=-1)

    @staticmethod
    def get_file_md5(file_path):
        return hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    def list_source_image_file(self):
        """列出源文件"""
        return self.list_file(self.source_dir, ignore_compressed=False)

    def list_need_compress_file(self):
        """列出需要压缩的文件"""
        return self.list_file(self.source_dir, ignore_compressed=True)

    def list_file(self, dir_path, ignore_compressed=True):
        # jpg 或 png，但不包括 .9.png
        files = filex.list_file(dir_path, '(jpg)|((?<!\.9\.)png)$')
        print(f'过滤掉非图片文件，还剩 {len(files)} 个')

        files = list(filter(self.not_in_keep_files, files))
        print(f'过滤掉保留的文件，还剩 {len(files)} 个')

        files = list(filter(lambda x: os.path.getsize(x) >= self.minimum_size, files))
        print(f'过滤掉小于 {self.minimum_size} 的文件，还剩 {len(files)} 个')

        if ignore_compressed:
            files = list(filter(self.not_compress_yet, files))
            print(f'过滤掉已压缩的文件，还剩 {len(files)} 个')

        return files

    def check_files(self, files, move=0):
        """
        检查文件
        :param files: 文件
        :param move: 是否移动
        0 不移动
        1 将结果文件覆盖源文件
        -1 将源文件覆盖目录文件
        :return:
        """
        length = len(files)
        remain_file = 0
        for i in range(self.offset, length):
            file = files[i]
            source_file_length = os.path.getsize(file)
            target_file = self.get_target_file(file)
            if move == -1:
                # 为 -1 的时候是复制到目标目录
                print(f'复制 {file} -> {target_file}')
                self.copy_file(file, target_file)
                continue
            if not os.path.exists(target_file):
                print(f'结果文件不存在 {target_file}')
                remain_file += 1
                continue
            target_file_length = os.path.getsize(target_file)

            source_size = filex.parse_file_size(source_file_length)
            target_size = filex.parse_file_size(target_file_length)
            reduce_length = source_file_length - target_file_length
            reduce_size = filex.parse_file_size(reduce_length)
            reduce_percent = reduce_length / source_file_length * 100
            print(f'{i + 1}/{length} {source_size} -> {target_size},减小 {reduce_percent:.2f}%,{reduce_size}, {file}')
            if move == 1:
                print(f'复制 {target_file} -> {file}')
                self.copy_file(target_file, file)
        print(f'剩余文件 {remain_file} 个')

    def not_in_keep_files(self, file):
        """不是保留的文件"""
        if self.keep_files:
            for keep_file in self.keep_files:
                file_name = os.path.basename(file)
                file_name = os.path.splitext(file_name)[0]
                if re.fullmatch(keep_file, file_name):
                    print(f'过滤文件 {file}')
                    return False
        return True

    def not_compress_yet(self, file):
        """尚未压缩"""
        return not os.path.exists(self.get_target_file(file))

    def get_target_file(self, source_file):
        return source_file.replace(self.source_dir, self.target_dir)

    def compress_first_file(self):
        files = self.list_need_compress_file()
        self.compress_image(files[0])

    def compress_all_file_in_loop(self):
        files = self.list_need_compress_file()
        length = len(files)
        for i in range(self.offset, length):
            print(f'压缩每 {i + 1}/{length} 张图片')
            self.compress_image(files[i])

    def compress_all_file_in_thread(self):
        files = self.list_need_compress_file()
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

    def generate_md5_of_current_source_files(self, md5_file):
        """生成当前所有源文件的 md5"""
        files = self.list_source_image_file()
        lines = []
        for file in files:
            md5 = self.get_file_md5(file)
            lines.append(f'{md5},{file}')
        filex.write_lines(md5_file, lines, add_line_separator=True)

    def copy_tiny_png_by_md5(self, md5_file, reference_target_dir):
        """
        根据文件的 md5 复制已压缩的文件
        如果存在 md5 ，如果在参考目标目录中有结果文件，则直接将其复制到结果目录中
        :param md5_file: md5 文件
        :param reference_target_dir:参考目标目录
        :return:
        """
        lines = filex.read_lines(md5_file, ignore_line_separator=True)
        if not lines:
            print('没有 md5')
            return
        md5_dict = {}
        for line in lines:
            md5, path = line.split(',')
            md5_dict[md5] = path
        files = self.list_need_compress_file()
        for file in files:
            md5 = self.get_file_md5(file)
            if not (md5 in md5_dict.keys()):
                continue
            reference_source_file = md5_dict[md5]
            reference_target_file = reference_source_file.replace(self.source_dir, reference_target_dir)
            if not os.path.exists(reference_target_file):
                # 不存在参考文件
                print(f'已压缩文件不存在 {reference_target_file}')
                continue
            target_file = self.get_target_file(file)
            print(f'文件相同，复制已压缩文件 {reference_target_file} -> {target_file}')
            self.copy_file(reference_target_file, target_file)

    def copy_file(self, source, target):
        """复制文件"""
        filex.check_and_create_dir(target)
        source_md5 = self.get_file_md5(source)
        target_md5 = self.get_file_md5(target)
        if source_md5 == target_md5:
            print('文件已相同')
        else:
            shutil.copyfile(source, target)


if __name__ == '__main__':
    TinyPng('',
            source_dir=r'',
            target_dir=r'',
            minimum_size=1024,
            keep_files=None,
            offset=0).main()
