import re

from xx import filex
from xx import iox


class ModifyApi:
    """项目中统一修改 api 地址"""

    def __init__(self, path):
        self.path = path

    def main(self):
        action_list = [
            ['退出', exit],
            ['修改 api', self.modify_api],
        ]
        iox.choose_action(action_list)

    def modify_api(self):
        lines = filex.read_lines(self.path, ignore_line_separator=True)
        if not lines:
            print(f'行为空')
            return

        changed_apis = self.get_changed_apis()
        if not changed_apis:
            print(f'api 为空')
            return
        changed_dealer_apis = self.get_changed_apis(True)
        if not changed_dealer_apis:
            print(f'dealer api 为空')
            return

        # 开始处理
        new_lines = []
        api_urls = []
        # 以空格开头，@ 加method，( ，可能带dealder，)
        pattern = re.compile(r'\s+@(\w+)\((.*)"(.+)"\)$')
        for i, line in enumerate(lines):
            line = line.replace('\n', '')
            match = pattern.match(line)
            if not match:
                # 不匹配直接添加
                new_lines.append(line)
                continue

            api_urls.append(line)
            print(f'处理第 {len(api_urls)} 个 {line}')

            method, add, url = match.groups()
            if 'DEALER' in add:
                # dealer 的
                new_url = self.modify_line(url, changed_dealer_apis)
            else:
                # api 的
                new_url = self.modify_line(url, changed_apis)
            if url == new_url:
                new_lines.append(line)
                print(f'没有变化')
            else:
                new_lines.append(line.replace(url, new_url))
                print(f'变为了 {new_url}')

        print(f'共 {len(api_urls)} 个 api')

        remain_apis = list(filter(lambda x: not x.replaced, changed_apis))
        print(f'有 {len(remain_apis)} 个接口未替换')
        for api in remain_apis:
            print(api.old)

        remain_apis = list(filter(lambda x: not x.replaced, changed_dealer_apis))
        print(f'有 {len(remain_apis)} 个 dealer 接口未替换')
        for api in remain_apis:
            print(api.old)

        # 保存文件
        filex.write_lines(self.path, new_lines, add_line_separator=True)

    def get_changed_apis(self, dealer=False):
        prefix = 'dealer_' if dealer else ''
        lines = filex.read_lines(f'ignore/{prefix}api.txt', ignore_line_separator=True)
        apis = []
        for line in lines:
            old, new = line.split('\t')
            old = old.strip('/')
            new = new.strip('/')
            # 去除开头的 dealer 等，已经添加到了 baseUrl 里
            new = new[new.index('/') + 1:]
            apis.append(Api(old, new))
        # 因为在 modify_line 会使用 startswith 来判断，因此如果按顺序，可以将较短的先匹配了
        # 比如 test testV2 将不会匹配到 testV2 因此倒序
        apis = sorted(apis, key=self.get_compare_key, reverse=True)
        return apis

    @staticmethod
    def get_compare_key(api):
        return api.old

    @staticmethod
    def modify_line(url: str, apis):
        for api in apis:
            if url == api.old:
                api.replaced = True
                print(f'url 等于旧地址 {api.old}，直接替换')
                return api.new
            elif url.startswith(api.old):
                api.replaced = True
                print(f'url 以旧地址 {api.old} 开头，替换开头')
                # 注意不能使用 replace
                return api.new + url[len(api.old):]
        print('没有找到')
        return url


class Api:
    def __init__(self, old, new):
        self.new = new
        self.old = old
        self.replaced = False


if __name__ == '__main__':
    ModifyApi(
        path=r''
    ).main()
