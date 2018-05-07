import hashlib
import urllib.parse
from xml.etree import ElementTree as Et

from xx import iox


class PhysicsBalls:
    """
    物理弹球的 sp 加密

    <string name="key_version">1.0</string>
    <string name="key_version_s">c1cd799023551f8eb3bcc805ff736717</string>
    """

    def __init__(self):
        self.iemi = 'vectorAlwaysLoveU' + 'vectorAlwaysLoveU'
        self.sp_file = 'ignore/game.color.ballz.block.brick.puzzle.free.physics.balls.xc.v2.playerprefs.xml'
        self.parsed_sp_file = 'ignore/parsed.xml'

        self.key_useInfo = 'key_useInfo'
        self.key_useInfo_s = 'key_useInfo_s'

    def main(self):
        action_list = [
            ['退出', exit],
            ['加密测试', self.encrypt_text, '1.0'],
            ['加密内容', self.input_and_encrypt],
            ['decode 存档', self.decode_file, self.sp_file, self.parsed_sp_file],
            ['保存存档', self.save_file, self.parsed_sp_file, self.sp_file]
        ]
        iox.choose_action(action_list)

    def decode_file(self, input_file, output_file):
        """ url decode 解码存档"""
        tree = Et.parse(input_file)
        root = tree.getroot()
        for string_element in root.iter('string'):
            name = string_element.attrib['name']
            if name == self.key_useInfo:
                print('%s is \n%s' % (self.key_useInfo, string_element.text))
                string_element.text = self.url_decode(string_element.text)
                print('解码为', string_element.text)
                break
        tree.write(output_file)
        print('保存到', output_file)

    def save_file(self, input_file, output_file):
        """ 保存存档"""
        tree = Et.parse(input_file)
        root = tree.getroot()
        # 保存用户信息加密结果
        use_info_s = ''
        for string_element in root.iter('string'):
            name = string_element.attrib['name']
            if name == self.key_useInfo:
                print('%s is \n%s' % (self.key_useInfo, string_element.text))
                # 对 encode 之前的内容计算 md5
                use_info_s = self.encrypt_text(string_element.text)
                string_element.text = self.url_encode(string_element.text)
                print('编码为', string_element.text)
                break
        # 如果是保存，还要修改
        for string_element in root.iter('string'):
            name = string_element.attrib['name']
            if name == self.key_useInfo_s:
                print('%s is \n%s' % (self.key_useInfo_s, string_element.text))
                string_element.text = use_info_s
                print('修改为', string_element.text)
                break
        tree.write(output_file)
        print('保存到', output_file)

    def input_and_encrypt(self):
        """输入并加密"""
        text = input('请输入要加密的内容\n')
        if text:
            self.encrypt_text(text)

    def encrypt_text(self, text):
        """
        PlayerPrefs.SetString("key_" + type + "_s", md5(iemi + value + iemi));
        """
        print('加密', text)
        text = '%s%s%s' % (self.iemi, text, self.iemi)
        print('拼接为', text)
        result = self.md5(text)
        print('结果为', result)
        return result

    @staticmethod
    def md5(text):
        h = hashlib.md5()
        h.update(text.encode())
        return h.hexdigest()

    @staticmethod
    def url_encode(string):
        return urllib.parse.quote(string)

    @staticmethod
    def url_decode(string):
        return urllib.parse.unquote(string)


if __name__ == '__main__':
    PhysicsBalls().main()
