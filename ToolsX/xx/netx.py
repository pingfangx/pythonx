"""
联网相关
"""

import urllib.parse
import urllib.request


def get(url, params=None, headers=None, cookie=None, encode='utf-8', need_print=True):
    """
    获取数据
    :param url: 地址
    :param params: 参数
    :param headers： 头
    :param cookie: cookie
    :param encode: 编码
    :param need_print: 是否需要打印
    :return:
    """
    # 伪装头
    # Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
    ua = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    if headers is None or headers is not dict:
        headers = {
            'User-Agent': ua
        }
    else:
        if not 'User-Agent' in headers.keys():
            headers['User-Agent'] = ua

    # 拼接参数
    if params is not None:
        extra = urllib.parse.urlencode(params)
        if '?' in url:
            url += '&' + extra
        else:
            url += '?' + extra

    # 构建请求
    request = urllib.request.Request(
        url=url,
        headers=headers)

    # 打开请求
    if need_print:
        print("open " + url)
    if cookie is None:
        request_data = urllib.request.urlopen(request)
    else:
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', cookie))
        request_data = opener.open(request)

    # 读取并解析结果
    result = request_data.read().decode(encode)
    if need_print:
        print('result is ' + result)
    return result
