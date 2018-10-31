import os
import subprocess
import time

from selenium import webdriver


class VpnLogin:
    """
    vpn 登录不能记住密码
    写个小工具自动填写
    """
    user_file_path = os.path.dirname(__file__) + r'/ignore/user.txt'
    """第一行用户名，第二行密码"""
    home_page = 'https://vpn.00bang.net'
    vpn_process_name = 'SangforCSClient.exe'

    def __init__(self):
        with open(self.user_file_path) as f:
            lines = f.readlines()
            if len(lines) > 1:
                self.user_name = lines[0].strip('\n')
                self.password = lines[1].strip('\n')
        if not self.user_name or not self.password:
            print(f'未正确读取到用户名、密码，文件 {self.user_file_path}')
            exit(1)

    def check_and_login(self):
        """检查并登录"""
        if self.get_running_process_count(self.vpn_process_name) > 0:
            print('vpn running.')
            exit(0)
        else:
            print('vpn not running,start it.')
            self.login()

    @staticmethod
    def get_running_process_count(image_name):
        """获取正在运行的进程数"""
        cmd = f'tasklist /FI "IMAGENAME eq {image_name}"'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # 有中文，用 gbk 解码
        return process.stdout.read().decode('gbk').count(image_name)

    def login(self):
        """登录"""
        url = self.home_page
        print('open %s' % url)
        driver = webdriver.Chrome()
        driver.get(url)

        # 检查是否已登录
        page = driver.page_source
        if '您已经登录了VPN' in page:
            print('您已经登录了VPN')
            return

            # 填入用户名、密码并登录
        user_name = driver.find_element_by_id('svpn_name')
        user_name.send_keys(self.user_name)

        password = driver.find_element_by_id('svpn_password')
        password.send_keys(self.password)

        login_btn = driver.find_element_by_id('logButton')
        login_btn.click()

        print('点击登录')

        times = 0
        while times < 10:
            times += 1
            time.sleep(1)
            # 检查登录结果
            page = driver.page_source
            if '注销' in page:
                print('登录成功')
                print('3s 后关闭')
                # 避免客户端未启动
                time.sleep(3)
                return
        print('超时，未登录成功')
        exit(1)


if __name__ == '__main__':
    VpnLogin().check_and_login()
