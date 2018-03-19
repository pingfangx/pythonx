import requests
from bs4 import BeautifulSoup

"""
解析网页示例
"""


def parse_demo():
    r = requests.get('')
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find('input', {'name': 'authenticity_token'})['value']
