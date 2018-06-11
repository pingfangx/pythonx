import re

import requests
from bs4 import BeautifulSoup

from xx import excelx
from xx import filex
from xx import iox
from xx import netx

"""
使用方式
往文件 ignore/token.txt 中写入 token
往 issues.xlsx 中写入要处理的任务
相关字段见 Issue 类中的注释

最后先读取任务，确认无误后再上传
"""


class Issue:
    def __init__(self):
        self.filter = '过滤'
        """
        不用上传
        1 表示过滤，不处理
        """

        self.project = '项目'
        """
        不用上传
        用来拼接项目地址
        """

        self.tracker_id = '跟踪'
        """
<option value="1">错误</option>
<option value="2">任务</option>
<option value="3">建议</option>
        """

        self.subject = '主题'
        self.description = '描述'
        """可为空"""

        self.status_id = '状态'
        """
<option value="1">新建</option>
<option value="2">进行中</option>
<option value="3">已解决</option>
<option value="4">验证通过</option>
<option value="5">已关闭</option>
<option value="6">已拒绝</option>
        """

        self.assigned_to_id = '指派给'
        """需要指定为 id"""

        self.start_date = '开始日期'
        """格式为 YYYY-MM-dd"""

        self.due_date = '完成日期'
        self.done_ratio = '完成'
        """百分比，不带百分号"""

    def __str__(self):
        return '{%s}' % ','.join([k + '=' + v for k, v in self.__dict__.items()])

    def __repr__(self):
        return self.__str__()


class Redmine:
    def __init__(self):

        self.issue_list = None
        self.subject_prefix = '【Android】'
        """主题前缀"""

        self.redmine_url = 'http://redmine.00bang.net/redmine'
        self.project_url = self.redmine_url + '/projects/%s/issues'
        self.login_url = self.redmine_url + '/login'

        self.login_file = r'ignore/login.txt'
        self.cookies_file = r'ignore/cookies.txt'
        self.token_file = r'ignore/token.txt'
        self.params_file = r'params.txt'
        self.excel_file = r'issues.xlsx'

    def main(self):
        action_list = [
            ['退出', exit],
            ['登录', self.login, self.login_file],
            ['从 excel 读取任务', self.read_issue_from_excel, self.excel_file],
            ['上传任务', self.upload_issue]
        ]
        while True:
            iox.choose_action(action_list)

    def login(self, file_path):
        """登录并保存信息"""
        lines = filex.read_lines(file_path, ignore_line_separator=True)
        if not lines:
            print('没有读取到登录信息', file_path)
            exit()
        if len(lines) < 2:
            print('登录信息不完整，第一行写帐号，第二行写密码')
            exit()

        print('打开登录页...')
        r = requests.get(self.login_url)
        cookies, authenticity_token = self.parse_cookies_and_token_from_result(r)
        if not (cookies and authenticity_token):
            print('登录失败')
            return

        # 获取完 cookies, token ，开始登录
        params = {
            'username': lines[0],
            'password': lines[1],
            'utf8': '✓',
            'authenticity_token': authenticity_token,
        }
        print('登录帐号 %s ...' % lines[0])
        r = requests.post(self.login_url, params, cookies=cookies)
        # 注意 cookies 和 token 都要重新获取
        cookies, authenticity_token = self.parse_cookies_and_token_from_result(r)
        if not (cookies and authenticity_token):
            print('登录失败')
            return
        print('登录成功')
        cookies_str = ';'.join([k + '=' + v for k, v in cookies.items()])
        filex.write(self.cookies_file, cookies_str)
        filex.write(self.token_file, authenticity_token)

    @staticmethod
    def parse_cookies_and_token_from_result(r):
        """从联网结果解析 cookies 和 token"""
        soup = BeautifulSoup(r.text, "html.parser")
        authenticity_token = soup.find('input', {'name': 'authenticity_token'})
        if authenticity_token:
            authenticity_token = authenticity_token['value']
        return r.cookies, authenticity_token

    def read_issue_from_excel(self, file_path):
        """读取任务"""
        data = excelx.read_from_excel(file_path)
        if not data:
            print('没有读取到数据', file_path)
            return
        title_line_index = 0
        first_data_line_index = title_line_index + 1
        title_line = data[title_line_index]
        issue = Issue()
        issue_fields = issue.__dict__
        for i in range(len(title_line)):
            title = title_line[i]
            for key, value in issue_fields.items():
                # values 没有 index of 方法，只好循环，不知道有没有好方法
                if title == value:
                    title_line[i] = key
                    break
        print('标题顺序')
        print(title_line)
        # 有了标题，接下来生成数据
        issue_list = []
        first_data_line = data[first_data_line_index]
        for i in range(first_data_line_index, len(data)):
            line = data[i]
            issue_fields = {}
            for j in range(len(title_line)):
                value = line[j]
                if i != first_data_line_index and value == '':
                    # 如果为空，以第一行为准
                    value = first_data_line[j]
                if isinstance(value, float):
                    # 取掉小数点
                    value = str(int(value))
                else:
                    value = str(value)
                issue_fields[title_line[j]] = value
            issue = Issue()
            issue.__dict__ = issue_fields
            # 添加主题前缀
            if not issue.subject.startswith(self.subject_prefix):
                issue.subject = self.subject_prefix + issue.subject
            issue_list.append(issue)
        self.issue_list = issue_list
        print('读取完成')
        for issue in self.issue_list:
            print(issue)

    def read_cookies_and_token_from_file(self):
        """从保存的文件读取"""
        cookies = netx.parse_cookies_from_file(self.cookies_file)
        if not cookies:
            print('读取 cookie 失败', self.cookies_file)

        token = filex.read(self.token_file)
        if not token:
            print('读取 token 失败', self.token_file)
        return cookies, token

    def upload_issue(self):
        """上传任务"""
        cookies, token = self.read_cookies_and_token_from_file()
        if not self.issue_list:
            print('没有任务列表，请先读取任务')
            return
        if not (cookies and token):
            exit()
        params = self.read_params(self.params_file)
        params['authenticity_token'] = token
        if not params:
            print('读取参数失败，参数文件', self.params_file)
            exit()
        print('默认参数为')
        print(params)

        for i in range(len(self.issue_list)):
            print()
            print('处理第 %d/%d 个任务' % (i + 1, len(self.issue_list)))
            issue = self.issue_list[i]
            if issue.filter == '1':
                print('已过滤')
                continue
            # copy 防止复用
            post_params = params.copy()
            url = self.project_url % issue.project
            for k, v in issue.__dict__.items():
                post_params['issue[%s]' % k] = v
            self.do_post(url, post_params, cookies)

    @staticmethod
    def do_post(url, params, cookies):
        print('post to', url)
        post_params = {}
        for key, value in params.items():
            post_params[key] = (None, value)
        # 这里也可以过滤掉不用上传的字段
        print(post_params)
        # 不跳转
        r = requests.post(url, cookies=cookies, files=post_params, allow_redirects=False)
        print('结果为')
        print(r.text)
        if re.search('You are being <a href="http://redmine/redmine/issues/\d+">redirected</a>', r.text):
            print('发布成功')
        else:
            print('发布失败')

    @staticmethod
    def read_params(file_path):
        lines = filex.read_lines(file_path, ignore_line_separator=True)
        if not lines:
            return None
        p = re.compile(r'name="(.*)"\t(.*)')
        result = {}
        for line in lines:
            match = re.search(p, line)
            if match:
                result[match.group(1)] = match.group(2)
        return result


if __name__ == '__main__':
    Redmine().main()
