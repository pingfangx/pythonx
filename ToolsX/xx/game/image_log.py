import os
import shutil
import time


class ImageLog:
    """图片记录"""

    def __init__(self, screenshot, max_count=100, debug=False):
        self.screenshot = screenshot
        self.max_count = max_count
        self.debug = debug

    def get_log_image(self, status, status_path, status_suffix=''):
        """获取记录图片的输出文件

        :param status: 状态
        :param status_path: 状态图片路径，用于分割出文件名
        :param status_suffix: 状态后缀，比如添加未找到
        :return:
        """
        if not self.debug:
            return None
        dir_name = self.get_log_image_dir()
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        filename = os.path.split(status_path)[1]
        filename = os.path.splitext(filename)[0]
        filename += status_suffix
        filename = time.strftime('%Y%m%d-%H%M%S-') + '%02d-%s.png' % (status, filename)
        file_path = os.path.join(dir_name, filename)
        return file_path

    def get_log_image_dir(self):
        """返回记录图片的路径"""
        dir_name = os.path.split(self.screenshot)[0]
        dir_name = os.path.join(dir_name, 'log')
        return dir_name

    def save_not_found_image(self, path):
        """保存未找到某状态的图片，方便排查"""
        if not self.debug:
            return None
        if os.path.exists(self.screenshot):
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            print(f'保存未找到状态图片到 {path}')
            shutil.copy(self.screenshot, path)

    def check_log_image_count(self):
        """检查日志图片的数量，超限则删除"""
        dir_name = self.get_log_image_dir()
        if os.path.exists(dir_name):
            files = os.listdir(dir_name)
            over_limit = len(files) - self.max_count
            if over_limit > 0:
                print(f'缓存图片超限了，删除 {over_limit}张')
                files = sorted(files)
                for i in range(over_limit):
                    file_path = os.path.join(dir_name, files[i])
                    print(f'删除 {file_path}')
                    os.remove(file_path)
