import os

import requests
from bs4 import BeautifulSoup

from xx import iox
from xx import netx


class CsdnAlbum:
    """
    csdn 专辑
    相关博文：http://blog.pingfangx.com/2457.html
    """

    def __init__(self, cookies, album_id):
        self.cookies = cookies
        self.album_id = album_id
        self.params = None

    def main(self):
        action_list = [
            ['退出', exit],
            ['获取专辑', self.get_album_info],
            ['编辑专辑', self.edit_album_info],
        ]
        while True:
            iox.choose_action(action_list)

    def get_album_info(self):
        """获取专辑信息"""
        url = 'http://download.csdn.net/addalbum/%d' % self.album_id
        page = netx.get(url, cookies=self.cookies, need_print=False)
        soup = BeautifulSoup(page, "html.parser")
        key_list = [
            'title',
            ('discription', 'textarea'),
            'tag',
            ('categorys', 'select'),
            ('category', 'select'),
            'type',
            'imagesrc',
            'ids',
            'album',
        ]
        params = dict()
        for key in key_list:
            # 处理 tag 名
            if len(key) == 2:
                key, tag_name = key
            else:
                tag_name = 'input'

            # 查找
            if key == 'type':
                # 要选中的
                key_tag = soup.find(tag_name, attrs={'name': key, 'checked': 'checked'})
            else:
                key_tag = soup.find(tag_name, attrs={'name': key})
            if not key_tag:
                print('没有找到 %s' % key)
                continue

            # 取值
            if key == 'imagesrc':
                value = None
            elif key == 'ids':
                value = list()
            elif 'value' in key_tag.attrs:
                value = key_tag['value']
            elif 'def' in key_tag.attrs:
                value = key_tag['def']
            else:
                value = key_tag.text
            params[key] = value

        # 读取 文件
        ul = soup.select_one('ul.add_source_list.items-list')
        a_list = ul.select('a.item')
        for a in a_list:
            params['ids'].append(a['id'])
        # 倒序排序
        params['ids'].sort(reverse=True)
        self.params = params
        print(params)

    def edit_album_info(self):
        """编辑专辑信息"""
        if not self.params:
            print('没有专辑信息')
            return
        post_params = dict()
        for key, value in self.params.items():
            post_params[key] = (None, value)
        post_params.pop('imagesrc')
        # 将数组拼接为字符串
        ids = ','.join(self.params['ids'])
        # ids = '10162219,10162217,10162215,10162213,10162211,10161369,10161367,10161363,10161361,10161357,10156949,10156944,10156940,10156934,10156925,10139011,10139006,10132432,10132429,10049974,10049970,10046862,10046857,10046853'
        # 注意前面的 name 还是要指定为 None
        post_params['ids'] = (None, ids)
        print(post_params)
        url = 'http://download.csdn.net/addalbum/create_album'
        result = requests.post(url, cookies=self.cookies, files=post_params)
        print(result.json())


if __name__ == '__main__':
    cookie_file = 'ignore/csdn_cookies.txt'
    if not os.path.exists(cookie_file):
        print('文件不存在 %s' % cookie_file)
        exit()
    with open(cookie_file, encoding='utf-8') as f:
        cookies_str = f.read()
        saved_cookies = netx.parse_cookies(cookies_str)
        CsdnAlbum(saved_cookies, 4157).main()
