import io
import os
import subprocess

from PIL import Image


class Adb:
    """ adb """

    def __init__(self, adb_path='adb', adb_params=None):
        """
        :param adb_path adb 路径，默认为 adb
        :param adb_params adb 参数，如 -s 指定设备
        """
        self.adb_path = adb_path
        """用于 adb devices 等命令"""

        self.adb_cmd = self.adb_path
        if adb_params is not None:
            self.adb_cmd += ' ' + adb_params
        """用于 adb 执行相关命令"""

        self.screen_type = 3
        """截图方式"""

    def test_device(self):
        """
        adb devices
        """
        print('检查设备是否连接...')
        # 这里使用 adb_path 其他命令使用 adb_cmd
        process = subprocess.Popen(self.adb_path + ' devices', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = process.communicate()
        print('adb 输出:')
        for each in output:
            print(each.decode('utf8'))

        result = output[0].decode('utf-8')
        title = 'List of devices attached'
        if result.startswith(title):
            result = result[len(title):]
            result = result.strip('\r\n')
            if not result:
                # 仅有标题，没有输出任何设备
                print('未找到设备')
                exit(1)
        print('设备已连接')

    def screenshot(self, screenshot_path=None, binary_screenshot=None):
        """截屏"""
        if self.screen_type == 0:
            # 截图
            screenshot_in_sdcard = '/sdcard/adb_screenshot.png'
            if screenshot_path is None:
                # 该截图方式必须要保存文件
                screenshot_path = 'ignore/screenshot.png'
            self.check_and_makedir(screenshot_path)
            self.run('shell screencap -p {}'.format(screenshot_in_sdcard))
            self.run('pull {} {}'.format(screenshot_in_sdcard, screenshot_path))
            print('截图保存至', screenshot_path)
            return Image.open(screenshot_path)
        else:
            if binary_screenshot is None:
                # 1-3 方式需要 binary_screenshot，如果失败直接作为参数传给下一个方法
                cmd = self.adb_cmd + ' shell screencap -p'
                print(cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                binary_screenshot = process.stdout.read()

            # 处理数据
            format_binary_screenshot = None
            if self.screen_type == 1:
                format_binary_screenshot = binary_screenshot
            elif self.screen_type == 2:
                format_binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
            elif self.screen_type == 3:
                format_binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')

            self.check_and_makedir(screenshot_path)
            # 解析图片
            try:
                image = Image.open(io.BytesIO(format_binary_screenshot))
                if screenshot_path and image:
                    image.save(screenshot_path)
                    print('截图保存至', screenshot_path)
                return image
            except OSError:
                self.screen_type -= 1
                return self.screenshot(screenshot_path, binary_screenshot)

    @staticmethod
    def check_and_makedir(file_path):
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def tap_position(self, position):
        """点击"""
        self.tap(*position)

    def tap(self, x, y):
        """点击"""
        self.shell_input('tap {} {}'.format(x, y))

    def swipe(self, x1, y1, x2, y2, duration=''):
        """滑动,ms"""
        self.shell_input('swipe {} {} {} {} {}'.format(x1, y1, x2, y2, duration))

    def back(self):
        """按返回"""
        self.shell_input('keyevent 4')

    def shell_input(self, cmd):
        """拼接 shell input"""
        self.run('shell input ' + cmd)

    def run(self, raw_command):
        """执行"""
        command = '{} {}'.format(self.adb_cmd, raw_command)
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read()
        return output
