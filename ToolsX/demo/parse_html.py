import requests
from bs4 import BeautifulSoup

"""
解析网页示例
"""


def parse_demo():
    r = requests.get('')
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find('input', {'name': 'authenticity_token'})['value']


def bs4():
    """相关方法"""
    soup = BeautifulSoup('text', 'html.parser')

    # 通过 class 查找
    soup.find_all('div', class_='class')

    # 通过 selector 选择
    soup.select('div.class')
    div = soup.select_one('div.class')

    # 取属性
    attr = div.attrs['attr']
    attr = div['attr']

    # 取内容
    text = div.get_text()
    text = div.text
