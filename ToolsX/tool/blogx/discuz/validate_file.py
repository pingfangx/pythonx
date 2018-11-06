import os
import shutil

from xx import iox, filex


class ValidateFile:
    """
    discuz 校验文件
    工具 > 文件校验
    校验结果作为文本复制出来
    """

    def __init__(self, source_dir, root_dir):
        self.source_dir = source_dir
        self.root_dir = root_dir
        self.result_path: dict = {
            '修改': 'modified',
            '删除': 'deleted',
            '添加': 'added',
        }

    def main(self):
        action_list = [
            ['退出', exit],
            ['输出检查结果', self.print_validate_result],
            ['备份增改的文件', self.backup_added_and_modified_file],
            ['还原添加的文件', self.backup_added_and_modified_file, True, '添加', False],
            ['还原修改的文件', self.backup_added_and_modified_file, True, '修改', False],
        ]
        iox.choose_action(action_list)

    def print_validate_result(self):
        """输出检查结果"""
        for name, key in self.result_path.items():
            path = self.get_validate_result_name(key)
            print(f'检查 {name} 的文件: {path}')
            dir_list, file_list = self.pares_files(path)
            print(f'共 {len(dir_list)} 个目录，{len(file_list)} 个文件')
            print(file_list)

    def backup_added_and_modified_file(self, reverse=False, check_name='', debug=False):
        """备份或还原增改的文件"""
        for name, key in self.result_path.items():
            path = self.get_validate_result_name(key)
            if check_name == '' or check_name == name:
                print(f'备份 {name} 的文件: {path}')
                dir_list, file_list = self.pares_files(path)
                print(f'共 {len(dir_list)} 个目录，{len(file_list)} 个文件')
                for file in file_list:
                    source_file = os.path.join(self.source_dir, file)
                    target_file = os.path.join(self.root_dir, key, file)
                    if reverse:
                        source_file, target_file = target_file, source_file
                    print('[debug]' if debug else '[do]' + f' {source_file} -> {target_file}')
                    if not debug:
                        filex.check_and_create_dir(target_file)
                        if os.path.isfile(source_file):
                            shutil.copy(source_file, target_file)
                        else:
                            if os.path.exists(target_file):
                                print('删除' + target_file)
                                shutil.rmtree(target_file)
                            shutil.copytree(source_file, target_file)

    def get_validate_result_name(self, key):
        return os.path.join(self.root_dir, key + '.txt')

    @staticmethod
    def pares_files(file_path):
        """解析文件"""
        dir_list = []
        file_list = []
        lines = filex.read_lines(file_path, ignore_line_separator=True)
        current_dir = ''
        for line in lines:
            if ':' in line:
                # 有时间，是文件
                is_dir = False
            else:
                if line == '.' or '/' in line or '.' not in line:
                    # 不包含“.” 视为文件，但是也有少数文件如 “install”
                    is_dir = True
                else:
                    is_dir = False
            if is_dir:
                current_dir = line
            else:
                # 是文件
                if current_dir not in dir_list:
                    dir_list.append(current_dir)
                file_name = line.split('\t')[0]
                file_path = f'{current_dir}/{file_name}'
                if file_path.startswith('./'):
                    file_path = file_path[2:]
                file_list.append(file_path)
        return dir_list, file_list


if __name__ == '__main__':
    p_source_dir = r'D:\workspace\PHPX\www.pingfangx.com\wwwroot'
    p_root_dir = 'ignore/x3.2/'
    ValidateFile(p_source_dir, p_root_dir).main()
