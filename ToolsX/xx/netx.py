"""
联网相关
"""

import os

import requests


def get(url, params=None, headers=None, cookies=None, encoding='utf-8', result_type='text', need_print=True):
    """
    获取数据
    :param url: 地址
    :param params: 参数
    :param headers： 头
    :param cookies: cookies
    :param encoding: 编码
    :param result_type: 结果类型
    :param need_print: 是否需要打印
    :return:
    """
    # 伪装头
    # Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
    ua = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    if headers is None or not isinstance(headers, dict):
        headers = {
            'User-Agent': ua
        }
    else:
        if not 'User-Agent' in headers.keys():
            headers['User-Agent'] = ua
    # 打开请求
    if need_print:
        print("open " + url)
        if params is not None:
            print('params', params)
    result = requests.get(url, params=params, headers=headers, cookies=cookies)
    result.encoding = encoding
    if result_type == 'text':
        result = result.text
    elif result_type == 'json':
        result = result.json()
    if need_print:
        print(f'result is {result_type}\n{result}')
    return result


def get_file(url, file_path, need_print=True, **kwargs):
    """下载文件"""
    if need_print:
        print('下载文件 %s ，从 %s' % (file_path, url))
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        if need_print:
            print('创建目录 %s' % dir_name)
    r = requests.get(url, None, **kwargs)
    with open(file_path, 'wb') as f:
        f.write(r.content)
    if need_print:
        print('下载完成')


def parse_cookies_from_file(file_path, exit_if_not_exists=True):
    """
    从文件中解析 cookies
    :param file_path: 文件路径
    :param exit_if_not_exists:文件不存在时，是否退出
    :return:
    """
    if not os.path.exists(file_path):
        print('cookies file not exists:', file_path)
        if exit_if_not_exists:
            exit()
        else:
            return
    with open(file_path, encoding='utf-8') as f:
        return parse_cookies(f.read())


def parse_cookies(cookies=''):
    """从字符串中解析出 cookies"""
    result = dict()
    if not cookies:
        return result

    key_value_list = cookies.split(';')
    for key_value in key_value_list:
        key_value_pair = key_value.split('=', maxsplit=1)
        if len(key_value_pair) == 2:
            key, value = key_value_pair
            result[key.strip()] = value.strip()
    return result


def parse_params_from_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        return parse_params(f.read())


def cookies_to_str(cookies):
    """转 cookies 为字符串"""
    return ';'.join([k + '=' + v for k, v in cookies.items()])


def parse_params(params):
    """
    解析参数，从 fiddler 中抓取后直接复制
    以 # 开头或者空行将被忽略
    """
    data = {}
    for line in params.split('\n'):
        if line.startswith('#'):
            continue
        if '\t' not in line:
            continue
        key, value = line.split('\t')
        data[key] = value
    return data


def handle_result(request, success_callback=None, fail_callback=None, print_result=True):
    """处理结果"""
    result = request.json()
    if print_result:
        print(result)
    if result:
        code = result['code']
        if code == 200:
            # 成功
            data = result['data']
            if success_callback:
                success_callback(data)
            return data
        else:
            # 失败
            msg = result['msg']
            print(msg)
            if fail_callback:
                fail_callback(code, msg)
    else:
        # 结果为空
        if fail_callback:
            fail_callback(0, None)
    return None
