import re

import netx
import requests
from xx import excelx
from xx import filex
from xx import iox

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
    def __init__(self, token, cookies):
        self.token = token
        self.cookies = cookies
        "用于认证"

        self.issue_list = None
        self.subject_prefix = '【Android】'
        """主题前缀"""

        self.project_url = 'http://redmine.00bang.net/redmine/projects/%s/issues'

        self.params_file = r'params.txt'
        self.excel_file = r'issues.xlsx'

    def main(self):
        action_list = [
            ['退出', exit],
            ['从 excel 读取任务', self.read_issue_from_excel, self.excel_file],
            ['上传任务', self.upload_issue]
        ]
        while True:
            iox.choose_action(action_list)

    def read_issue_from_excel(self, file_path):
        """读取任务"""
        data = excelx.read_from_excel(file_path)
        if not data:
            print('没有读取到数据', file_path)
            return
        title_line = data[0]
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
        for i in range(1, len(data)):
            line = data[i]
            issue_fields = {}
            for j in range(len(title_line)):
                if isinstance(line[j], float):
                    # 取掉小数点
                    value = str(int(line[j]))
                else:
                    value = str(line[j])
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

    def upload_issue(self):
        """上传任务"""
        if not self.issue_list:
            print('没有任务列表')
            return

        params = self.read_params(self.params_file)
        params['authenticity_token'] = self.token
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
            self.do_post(url, post_params)

    def do_post(self, url, params):
        print('post to', url)
        post_params = {}
        for key, value in params.items():
            post_params[key] = (None, value)
        # 这里也可以过滤掉不用上传的字段
        print(post_params)
        # 不跳转
        r = requests.post(url, cookies=self.cookies, files=post_params, allow_redirects=False)
        print('结果为')
        print(r.text)
        # TODO 这里要解析结果

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
    token_file = r'ignore/token.txt'
    saved_token = filex.read(token_file)
    if not saved_token:
        print('读取 token 失败', token_file)
        exit()

    cookies_file = r'ignore/cookies.txt'
    saved_cookies = filex.read(cookies_file)
    if not saved_cookies:
        print('读取 cookie 失败', cookies_file)
        exit()
    Redmine(saved_token, netx.parse_cookies(saved_cookies)).main()
