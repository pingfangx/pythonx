import hashlib
import re

from xx import iox


class GradleHelper:
    """
    相关博文 http://blog.pingfangx.com/2361.html
    """

    def main(self):
        action_list = [
            ['退出', exit],
            ['输入并计算 base36', self.calculate_base36],
            ['测试 base36', self.test_base36],
        ]
        iox.choose_action(action_list)

    def test_base36(self):
        """测试"""
        print(self.calculate_base36('3.3'))
        print(self.calculate_base36('3.3-all'))
        print(self.calculate_base36('3.3-all.zip'))
        print(self.calculate_base36('gradle-3.3-all.zip'))
        print(self.calculate_base36('https://services.gradle.org/distributions/gradle-3.3-all.zip'))
        print(self.calculate_base36(''))

    @staticmethod
    def calculate_base36(url=None):
        if not url:
            url = input('请输入地址，如 https://services.gradle.org/distributions/gradle-3.3-all.zip\n或版本号，如 3.3-all\n')
        if not url:
            print('url 为空')
            exit()
        if 'http' not in url:
            # 不以 http 开头认为需要补全，否则认为已经完整
            if re.match('^\d', url):
                # 以数字开头
                url = 'gradle-' + url
            if not url.endswith('.zip'):
                if not re.search('-(all|src|bin)', url):
                    # 不包含
                    url += '-all.zip'
                else:
                    url += '.zip'
            url = 'https://services.gradle.org/distributions/' + url
        return GradleHelper.calculate_base36_final(url)

    @staticmethod
    def calculate_base36_final(url=None):
        print('url is %s' % url)

        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        md5 = m.hexdigest()
        print('md5 is %s' % md5)

        number = int('0x' + md5, 16)
        print('number is %s' % number)

        base36 = GradleHelper.base36encode(number)
        print('base36 is %s' % base36)

        return base36

    @staticmethod
    def base36encode(integer):
        """
        from https://en.wikipedia.org/wiki/Base36#Python_implementation
        """
        chars, encoded = '0123456789abcdefghijklmnopqrstuvwxyz', ''

        while integer > 0:
            integer, remainder = divmod(integer, 36)
            encoded = chars[remainder] + encoded

        return encoded


if __name__ == '__main__':
    GradleHelper().main()
