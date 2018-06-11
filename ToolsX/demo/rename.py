import os

from xx import filex
from xx import iox


class Rename:
    def main(self):
        action_list = [
            ['退出', exit],
            ['重命名', self.rename, r'C:\Users\Administrator\Desktop\照片\平方X'],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def rename(dir_path):
        files = filex.list_file(dir_path)
        length = len(files)
        for i in range(length):
            file_path = files[i]
            new_path = dir_path + os.path.sep + '平方X-%02d%s' % (i + 1, os.path.splitext(file_path)[1])
            print('%s -> %s' % (file_path, new_path))
            os.rename(file_path, new_path)


if __name__ == '__main__':
    Rename().main()
