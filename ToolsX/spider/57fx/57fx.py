import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from xx import filex
from xx import iox


class Demo:
    """用来抓一些分享的视频的百度云"""

    def __init__(self):
        self.url_list_file = r'ignore/url_list.txt'
        self.pan_list_file = r'ignore/pan_list.txt'
        self.driver = None

    def main(self):
        action_list = [
            ['退出', exit],
            ['抓取各页地址', self.get_by_page],
            ['抓取网盘地址', self.iter_pan_url],
            ['打开浏览器', self.open_browser],
            ['保存文件到百度网盘', self.iter_save_pan],
        ]
        while True:
            iox.choose_action(action_list)

    def get_by_page(self, page=1):
        url = 'http://www.57fx.com/userinfo-1093677596-%d/' % page
        print('打开', url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.select_one('div.content.col.c_r')
        dd_list = content.find_all('dd')
        url_list = []
        for dd in dd_list:
            a = dd.select_one('div').select_one('a')
            url_list.append(a['href'])
        print(url_list)
        filex.write_lines(self.url_list_file, url_list, mode='a', add_line_separator=True)
        if page < 5:
            self.get_by_page(page + 1)
        else:
            print('结束')

    def iter_pan_url(self):
        """从每一页中读取百度网盘地址"""
        lines = filex.read_lines(self.url_list_file, ignore_line_separator=True)
        length = len(lines)
        for i in range(length):
            print('获取 %d/%d' % (i + 1, length))
            self.get_pan_url(lines[i])

    def get_pan_url(self, url):
        url = 'http://www.57fx.com' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        a = soup.find('a', {'name': 'downurl'})
        href = a['href']
        filex.write(self.pan_list_file, href + '\n', mode='a')

    def open_browser(self):
        chrome_path = r'D:\software\browser\Chrome\Application\chrome.exe'
        print('启动 chrome')
        chrome_options = None
        if chrome_path:
            chrome_options = ChromeOptions()
            chrome_options.binary_location = chrome_path
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def iter_save_pan(self):
        """保存进百度网盘"""
        lines = filex.read_lines(self.pan_list_file, ignore_line_separator=True)
        length = len(lines)
        for i in range(length):
            print('保存 %d/%d' % (i + 1, length))
            self.save_pan_url(lines[i], self.driver)
        print('结束')
        # driver.quit()

    @staticmethod
    def save_pan_url(url, driver):
        """点击保存有时会出错，不好用，手动点则不会，可能是使用 driver 的问题"""
        print(url)
        driver.get(url)
        element = driver.find_element_by_css_selector('a.g-button.g-button-blue')
        print('点击保存')
        element.click()
        time.sleep(2)
        element = driver.find_element_by_css_selector('a.g-button.g-button-blue-large')
        element.click()
        print('点击确定')
        time.sleep(2)


if __name__ == '__main__':
    Demo().main()
