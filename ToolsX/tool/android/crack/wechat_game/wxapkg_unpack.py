import os
import struct


class WxapkgFile:
    nameLen = 0
    name = ""
    offset = 0
    size = 0


class WxapkgUnpack:
    """
    微信小程序解包

    原作者为 [lrdcq《微信小程序源码阅读笔记1》](http://lrdcq.com/me/read.php/66.htm)
    jin10086 将其转为了 Python3 [wxgameHacker](https://github.com/jin10086/wxgameHacker)
    我又找了原作者的代码转为 Python3 ，仅修改了变量名等
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def main(self):
        with open(self.file_name, "rb") as f:
            root = os.path.dirname(os.path.realpath(f.name))
            name = os.path.basename(f.name)

            # read header

            first_mark = struct.unpack('B', f.read(1))[0]
            print('first header mark = ' + str(first_mark))

            info1 = struct.unpack('>L', f.read(4))[0]
            print('info1 = ' + str(info1))

            index_info_length = struct.unpack('>L', f.read(4))[0]
            print('index_info_length = ' + str(index_info_length))

            body_info_length = struct.unpack('>L', f.read(4))[0]
            print('body_info_length = ' + str(body_info_length))

            last_mark = struct.unpack('B', f.read(1))[0]
            print('last header mark = ' + str(last_mark))

            if first_mark != 190 or last_mark != 237:
                print('its not a wxapkg file!!!!!')
                exit()

            file_count = struct.unpack('>L', f.read(4))[0]
            print('file_count = ' + str(file_count))

            # read index

            file_list = []

            for i in range(file_count):
                data = WxapkgFile()
                data.nameLen = struct.unpack('>L', f.read(4))[0]
                # 这里 python2 为 data.name = f.read(data.nameLen)
                data.name = str(f.read(data.nameLen), encoding='utf-8')
                data.offset = struct.unpack('>L', f.read(4))[0]
                data.size = struct.unpack('>L', f.read(4))[0]

                print('readFile = ' + data.name + ' at Offset = ' + str(data.offset))

                file_list.append(data)

            # save files

            for d in file_list:
                d.name = '/' + name + '.unpack' + d.name
                path = root + os.path.dirname(d.name)

                if not os.path.exists(path):
                    os.makedirs(path)

                # 这里 python 2 为 w = open(root + d.name, 'w')
                w = open(root + d.name, 'wb')
                f.seek(d.offset)
                w.write(f.read(d.size))
                w.close()

                print('writeFile = ' + root + d.name)

            f.close()


if __name__ == '__main__':
    file_path = r'data/wx7c8d593b2c3a7703_3.wxapkg'
    WxapkgUnpack(file_path).main()
