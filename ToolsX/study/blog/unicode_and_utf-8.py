from xx import iox


class Demo:
    def main(self):
        action_list = [
            ['退出', exit],
            ['unicode_to_utf_8', self.unicode_to_utf_8, '一'],
            ['八进制 utf-8 转 unicode', self.octal_utf_8_to_unicode_with_split_dir,
             r'\350\275\246\345\217\213\344\274\232/\350\275\246\345\217\213\344\274\232\346\240\207\346\263\250'],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def unicode_to_utf_8(text: str):
        """
一
十六进制
0x4e00
二进制
0b100111000000000
01001110 00000000
用 utf-8 表示
11100100 10111000 10000000
二进制
0b11100100 10111000 10000000
十六进制
0xe4b880
b'\xe4\xb8\x80
        """
        print(text)

        hex_form = hex(ord(text))
        print('十六进制')
        print(hex_form)

        bin_form = bin(int(hex_form, 16))
        print('二进制')
        print(bin_form)

        bin_form = bin_form[2:]
        length = len(bin_form)
        if length < 16:
            bin_form = '0' * (16 - length) + bin_form
        print(bin_form[0:8], bin_form[8:])

        utf_8_bin_form = f'1110{bin_form[0:4]} 10{bin_form[4:10]} 10{bin_form[10:]}'
        print('用 utf-8 表示')
        print(utf_8_bin_form)

        print('二进制')
        print('0b' + utf_8_bin_form)

        utf_8_bin = eval('0b' + utf_8_bin_form.replace(' ', ''))

        print('十六进制')
        print(hex(utf_8_bin))

        print(text.encode('utf-8'))

    def octal_utf_8_to_unicode_with_split_dir(self, text: str):
        """先分隔目录"""
        text_list = text.split('/')
        print('各级目录')
        print(text_list)
        result = []
        for text in text_list:
            # 每级目录的文字
            result.append(self.octal_utf_8_to_unicode(text))
        print('/'.join(result))

    def octal_utf_8_to_unicode(self, text: str):
        """
        八进制的 utf-8 转为 unicode
        如 git 终端的转义
        """

        print(text)
        words = text.split('\\')
        words = list(filter(lambda x: x, words))
        words = [hex(int(x, 8))[2:] for x in words]
        print(words)

        utf_8_hex_form = '0x' + ''.join(words)
        print(f'utf-8 十六进制 {utf_8_hex_form}')

        utf_8_bin_form = bin(eval(utf_8_hex_form))
        print(f'utf-8 二进制 {utf_8_bin_form}')

        print('按 8 位分隔')
        unicode_bin_form_list = self.utf_8_bin_to_unicode_bin(utf_8_bin_form)
        print('8 位分隔结果')
        print(unicode_bin_form_list)

        result = ''
        for bin_form in unicode_bin_form_list:
            result += self.bin_to_unicode(bin_form)

        return result

    @staticmethod
    def utf_8_bin_to_unicode_bin(bin_form: str):
        """utf-8 的二进制按规则转为 unicode 二进制"""
        if bin_form.startswith('0b'):
            bin_form = bin_form[2:]

        # 按 8 位划分
        bin_form_list = []
        length = len(bin_form)
        for i in range(0, length, 8):
            bin_form_list.append(bin_form[i:i + 8])
        print(bin_form_list)

        # 合并
        result_list = []
        length = len(bin_form_list)
        i = 0
        while i < length:
            bin_form = bin_form_list[i]
            # 第一个字节的 1 的数量表示几个字节
            bytes_length = bin_form.index('0')
            result = bin_form[bytes_length + 1:]
            for j in range(i + 1, i + bytes_length):
                result += bin_form_list[j][2:]
            print(result)
            result_list.append(result)
            i += bytes_length
        return result_list

    @staticmethod
    def bin_to_unicode(bin_form: str):
        """二进制转为 unicode"""

        if not bin_form.startswith('0b'):
            bin_form = '0b' + bin_form
        print(f'二进制 {bin_form}')

        unicode_decimal_form = eval(bin_form)
        print(f'unicode 十进制 {unicode_decimal_form}')

        unicode_hex_form = hex(unicode_decimal_form)
        print(f'unicode 十六进制 {unicode_hex_form}')

        result = chr(unicode_decimal_form)
        print(f'最终结果 {result}')
        return result


if __name__ == '__main__':
    Demo().main()
