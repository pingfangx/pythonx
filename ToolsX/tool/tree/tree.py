import os
from xx import iox
from xx import filex


class Tree:
    def main(self):
        blogx_file = 'data/blogx.txt'
        action_list = [
            ['退出', exit],
            ['读取并显示文件', self.read_and_show, blogx_file],
            ['读取并创建文件夹', self.read_and_create_folders, blogx_file],
            ['重启explorer进程', self.restart_explorer],
        ]
        iox.choose_action(action_list)

    def read_and_show(self, file_path):
        """
        读取文件
        :param file_path: 文件路径
        :return: 
        """
        data = self.get_tree_data_from_file(file_path)
        if data is not None:
            print(self.parse_data_to_tree_text(data))

    def read_and_create_folders(self, file_path):
        """
        读取并创建文件夹
        :return: 
        """
        data = self.get_tree_data_from_file(file_path)
        if data is not None:
            self.create_folders(data)

    def restart_explorer(self):
        """
        重启浏览器进程
        :return: 
        """
        self.run_command('taskkill /f /im explorer.exe')
        self.run_command('start explorer.exe ')

    def create_folders(self, data, pre='', write_comment=False):
        if not data:
            return
        size = len(data)
        if not size:
            return
        for i in range(size):
            folder = data[i]
            name = folder.name
            child = folder.child
            comment = folder.comment
            # 输出名字
            file_path = pre + name
            print('创建' + file_path + (',备注：' + comment if comment else ''))
            if not os.path.exists(file_path):
                os.mkdir(file_path)
                print('创建成功')
            else:
                print('文件夹已存在')
            if write_comment:
                if comment:
                    self.write_file_comment(file_path, comment)
            # 如果有child，递归
            if len(child) != 0:
                self.create_folders(child, pre + name + '/', write_comment)

    def write_file_comment(self, file_path, comment):
        """
        写入备注，参考https://github.com/piratf/windows-folder-remark
        :param file_path: 
        :param comment: 
        :return: 
        """
        file_folder = file_path
        file_path = file_path + '/'
        comment = comment
        if not file_path.endswith('/'):
            print('路径必须以/结尾')
            return
        ini_file = file_path + 'desktop.ini'
        shell_class_info_line = '[.ShellClassInfo]' + os.linesep
        tip_line_start = 'InfoTip='
        tip_line = tip_line_start + comment + os.linesep
        modify_info_line = False
        if not os.path.exists(ini_file):
            f = open(ini_file, 'w')
            f.close()
        f = open(ini_file, 'r')
        lines = f.readlines()
        if len(lines) == 0:
            # 不存在，直接写入
            lines.append(shell_class_info_line)
            lines.append(tip_line)
            modify_info_line = True
            print('直接写入备注')
        else:
            print('检查备注')
            # 存在，读取行
            find_shell_class_info_line = -1
            find_tip_line = -1
            for i in range(len(lines)):
                if lines[i] == shell_class_info_line:
                    find_shell_class_info_line = i
                elif lines[i].startswith(tip_line_start):
                    find_tip_line = i
                    if lines[i] != tip_line:
                        lines[i] = tip_line
                        modify_info_line = True
                        print('修改备注')
                    else:
                        print('备注已存在')
            if find_shell_class_info_line == -1:
                print('属性文件有错，不写入，应该为空，或者含' + shell_class_info_line)
            else:
                # 有那一行
                if find_tip_line == -1:
                    # 没有找到，插入，如果找到了，会检查是否要修改
                    lines.append(tip_line)
                    modify_info_line = True
                    print('插入备注')
        f.close()
        if modify_info_line:
            # 写入新的
            self.run_command('attrib ' + ini_file + ' -s -h')
            f = open(ini_file, 'w')
            f.writelines(lines)
            f.close()
            self.run_command('attrib ' + ini_file + ' +s +h')
            # 文件夹也需要，http://superuser.com/questions/882442
            self.run_command('attrib ' + file_folder + ' +s')
            print('设置备注完成')

    @staticmethod
    def run_command(command):
        """
        运行命令
        :param command: 
        :return: 
        """
        os.system(command)

    def get_tree_data_from_file(self, file_path):
        """
        从文件中读取tree数据
        :param file_path: 
        :return: 
        """
        lines = filex.read_lines(file_path)
        if lines is None:
            return None
        return self.get_tree_from_lines(lines)

    def parse_data_to_tree_text(self, data, pre='', is_last=True):
        """
        解析数据为树型样式的文字
        :param data: 数据
        :param pre: 前辍
        :param is_last: 是否是最后一个
        :return: 
        """
        size = len(data)
        # 如果后面还有一层，添加|，否则留空
        if is_last:
            pre += 4 * ' '
        else:
            pre += '│' + 3 * ' '

        text = ''
        for i in range(size):
            folder = data[i]
            name = folder.name
            child = folder.child
            comment = folder.comment
            # 输出名字
            if i == size - 1:
                symbol = '└─'
            else:
                symbol = '├'
            text += '\n%s%s─%s%s' % (pre, symbol, name, (',备注：' + comment if comment else ''))
            # 如果有child，递归
            if len(child) != 0:
                if i == size - 1:
                    text += self.parse_data_to_tree_text(child, pre, True)
                else:
                    text += self.parse_data_to_tree_text(child, pre, False)
        return text

    @staticmethod
    def get_tree_from_lines(lines):
        """
        从文件中读取tree
        :param lines: 所有的行
        :return: 
        """
        if not lines:
            return []
        data = []
        # 每一层保存为数组，当缩进时，添加到上一层的最后一个folder
        pre_level = 0
        current_level = 0
        # 添加一个到0位，这样0位只保存一个Folder，防止文件中第一层有多个
        data.append(Folder('root', []))
        for line in lines:
            line = line.replace(4 * ' ', '\t')
            current_level = line.count('\t') + 1
            line_content = line.strip('\n').strip('\t')
            if current_level > pre_level:
                # 增加一层，置为当前层次
                data.insert(current_level, Folder(line_content, []))
            elif current_level == pre_level:
                # 相同层，将当前folder添加到上一层，且置为新的folder
                if data[current_level]:
                    # 上一层次的child添加
                    data[current_level - 1].child.append(data[current_level])
                # 置为当前层次
                data[current_level] = Folder(line_content, [])
            else:
                # 层次减少，递归到当前位置
                while pre_level > current_level:
                    data[pre_level - 1].child.append(data[pre_level])
                    data.pop(pre_level)
                    pre_level -= 1
                # 将当前folder添加到上一层，且置为新的folder
                if data[current_level]:
                    # 上一层次的child添加
                    data[current_level - 1].child.append(data[current_level])
                # 置为当前层次
                data[current_level] = Folder(line_content, [])
            # 上一层赋值
            pre_level = current_level
        # 结束后，全部退到0位
        while current_level > 0:
            data[current_level - 1].child.append(data[current_level])
            data.pop(current_level)
            current_level -= 1
        # 只返回内容
        return data[0].child


class Folder:
    def __init__(self, name, child):
        result = name.split("'")
        self.name = result[0]
        if len(result) > 1:
            self.comment = result[1]
        else:
            self.comment = ''
        self.child = child


if __name__ == '__main__':
    Tree().main()
