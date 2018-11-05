import base64
import re
import time

from xx import iox, filex, encodex, netx


class DiscuzSource:
    """学习 discuz 的源码"""

    def __init__(self, config_file):
        """
        :param config_file: discuz 配置文件
        """
        self.config_file = config_file
        self.config_lines = []
        self.cookie_file = r'ignore/cookies.txt'
        self.cookies = {}

    def main(self):
        action_list = [
            ['退出', exit],
            ['生成 cookie_pre', self.generate_cookie_pre, True],
            ['生成 authkey', self.generate_authkey, True],
            ['输入并加密', self.input_and_auth_encode],
            ['测试解密', self.test_decode],
            ['测试访问', self.test_browse],
        ]
        iox.choose_action(action_list)

    def init_config(self):
        """读取配置，用来生成 cookiepre 、authkey 等"""
        if not self.config_lines:
            self.config_lines = filex.read_lines(self.config_file, ignore_line_separator=True)
        return self.config_lines

    def init_cookies(self):
        """读取 cookies"""
        if not self.cookies:
            self.cookies = netx.parse_cookies_from_file(self.cookie_file)
        return self.cookies

    def get_config(self, key: str):
        """获取配置"""
        key_array = key.split('.')
        name = '$_config'
        for k in key_array:
            name += f"['{k}']"
        config_lines = self.init_config()
        pattern = re.compile(f"^.*?\s*=\s*'(.*)';$")
        for line in config_lines:
            if line.startswith(name):
                match = re.match(pattern, line)
                if match:
                    return match.group(1)

    def generate_cookie_pre(self, print_msg=False):
        """
        使用 cookiepre , cookiepath , cookiedomain 生成 cookiepre
        $this->var['config']['cookie']['cookiepre'] =
        $this->var['config']['cookie']['cookiepre']
        .substr(md5($this->var['config']['cookie']['cookiepath']
        .'|'
        .$this->var['config']['cookie']['cookiedomain']), 0, 4)
        .'_';
        :return:
        """
        cookie_pre = self.get_config('cookie.cookiepre')
        cookie_path = self.get_config('cookie.cookiepath')
        cookie_domain = self.get_config('cookie.cookiedomain')
        t = cookie_path + '|' + cookie_domain
        t = encodex.md5(t)
        t = t[0:4]
        cookie_pre += t
        cookie_pre += '_'
        if print_msg:
            print(cookie_pre)
        return cookie_pre

    def generate_authkey(self, print_msg=False):
        """
        用于加密的 authkey
        $this->var['authkey'] = md5($this->var['config']['security']['authkey'].$this->var['cookie']['saltkey']);
        """
        saltkey = self.get_cookie('saltkey')
        t = self.get_config('security.authkey')
        t += saltkey
        t = encodex.md5(t)
        if print_msg:
            print(t)
        return t

    def get_cookie(self, key):
        """读取 cookie，自动添加 cookie pre"""
        return self.__get_cookie_from_file(self.generate_cookie_pre() + key)

    def __get_cookie_from_file(self, key):
        """从文件获取"""
        return self.init_cookies()[key]

    def input_and_auth_encode(self):
        """输入内容并加密"""
        text = input('请输入要加密内容\n')
        print(self.auth_encode(text))

    def test_decode(self):
        """测试解密"""
        auth = self.get_cookie('auth')
        auth = self.auth_decode(auth)
        print(auth)

    def test_browse(self):
        """
        测试访问
        通过学习加密我们知道，discuz 将相关内容保存在了 cookie 中
        解密时，没有过期时间，会一直解密成功，然后用密码去判断（该密码仅用于判断，与真实密码无关）
        cookie 是会失效的，但是如果我们将 cookie 保存下来，那么就可以一直使用了，永不失效（除非更改密码）。
        """
        url = 'http://localhost/'
        r = netx.get(url, need_print=False)
        if '退出' in r:
            print('已登录')
        else:
            print('未登录')

        r = netx.get(url, cookies=netx.parse_cookies_from_file(self.cookie_file), need_print=False)
        if '退出' in r:
            print('已登录')
        else:
            print('未登录')

    def auth_encode(self, text, key='', expiry=0):
        return self.authcode(text, operation='', key=key, expiry=expiry)

    def auth_decode(self, text, key='', expiry=0):
        return self.authcode(text, operation='DECODE', key=key, expiry=expiry)

    def authcode(self, string, operation='', key='', expiry=0):
        """
        将 php 翻译为 python，增强理解
        key 取的 authkey ，authkey 由配置的 authkey 和 saltkey 生成，每个人随机的 saltkey 不一致，保存在 cookie 中
        用 key 生成 crypkey 和 kaya,keyb
        keyc 用来加上时间，使得相同 key 的加密结果也不一致，但是为了解密，keyc 需要拼接在结果上
        时间拼在 0-10 用来记录时间，keyb 处理后拼在 10-16 用来校验完整性
        crypkey 生成密匙簿
        根据密匙簿进行异或处理，得出加密后的数据
        最后 base64.encode 并在前面拼上 keyc
        """
        ckey_length = 4
        if not key:
            key = self.generate_authkey()
        key = encodex.md5(key)
        keya = encodex.md5(key[0:16])
        keyb = encodex.md5(key[16:32])
        if ckey_length:
            if operation == 'DECODE':
                keyc = string[0:ckey_length]
            else:
                t = time.time()
                second = t / 1
                # 取微秒
                micro_time = 1 * 1000 * 1000 % 1000
                # microtime() 返回的格式
                t = f'{micro_time} {second}'
                t = encodex.md5(t)
                keyc = t[-ckey_length:]
        else:
            keyc = ''
        cryptkey = keya + encodex.md5(keya + keyc)
        key_length = len(cryptkey)
        if operation == 'DECODE':
            string = base64.b64decode(string[ckey_length:])
        else:
            # 时间
            t = 0
            if expiry:
                t = time.time() + expiry
            # 补齐 10 位
            t = '%010d' % t
            t2 = encodex.md5(string + keyb)[:16]
            # 前 10 位为时间，后 16 位为字符串+ keyb 取 md5 取 16 位，用来校验完整性
            string = t + t2 + string
        string_length = len(string)

        box = list(range(0, 256))

        # 产生密匙簿
        rndkey = [0] * 256
        for i in range(0, 256):
            rndkey[i] = ord(cryptkey[i % key_length])

        # 打乱密匙簿
        j = 0
        for i in range(0, 256):
            j = (j + box[i] + rndkey[i]) % 256
            box[i], box[j] = box[j], box[i]

        # 核心加解密部分
        a = 0
        j = 0
        byte_result = bytearray(string_length)
        for i in range(string_length):
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            box[a], box[j] = box[j], box[a]
            # 从密匙簿得出密匙进行异或，再转成字符
            if operation == 'DECODE':
                # decode 时，base64 解码出一个 bytes 数组，直接用 string[i] 取值
                t = string[i] ^ (box[(box[a] + box[j]) % 256])
            else:
                t = ord(string[i]) ^ (box[(box[a] + box[j]) % 256])
            byte_result[i] = t

        if operation == 'DECODE':
            result = byte_result.decode()
            t = int(result[0:10])
            # 校验时间
            if t == 0 or t - time.time() > 0:
                # 校验完整性，字符串加 keyb，取 md5 取 16 位
                t = result[26:]
                t += keyb
                t = encodex.md5(t)
                t = t[:16]
                if t == result[10:26]:
                    return result[26:]
                else:
                    return ''
            else:
                result = ''
        else:
            result = keyc + base64.b64encode(byte_result).decode().replace('=', '')
        return result


if __name__ == '__main__':
    p_config_file = r'D:\workspace\PHPX\discuz\config\config_global.php'
    DiscuzSource(p_config_file).main()
