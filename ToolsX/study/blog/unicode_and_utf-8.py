from xx import iox


class Demo:
    def main(self):
        action_list = [
            ['退出', exit],
            ['操作1', self.unicode_to_utf_8, '一'],
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


if __name__ == '__main__':
    Demo().main()
