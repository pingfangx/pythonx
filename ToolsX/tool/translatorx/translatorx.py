from typing import List, Callable

import common_utils
import software_utils
from software import Software


class TranslatorX:
    """翻译相关的工具类

    该类主要负责展示用户交互

    以前都是自己写了自用
    该脚本可能添加到仓库中，因此重写了一下。
    脚本应该

    独立
        不依赖于其他包，尽量可以独立运行
    可读
        尽量添加一点可读性
    """

    def __init__(self, config_file=''):
        self.software_list = software_utils.get_software_list(config_file)

    def main(self):
        action_list = [
            ['退出', exit],

            ['-汉化前的准备'],
            ['选择要操作的软件', self.check_software, self.software_list],
            ['i解压 jar 到 source 目录', software_utils.extract_jar_to_source_dir],
            ['i收集所有 tips 文件名', software_utils.collect_tip_names],

            ['-汉化后的操作'],
            ['i清空 target 目录', software_utils.clean_target_dir],
            ['i打包为汉化包', software_utils.zip_translation_jar],
            ['i将汉化包复制到软件 lib 目录', software_utils.copy_translation_to_work_dir],
            ['i打开软件', software_utils.open_software],

            ['-以下为一些工具方法'],
            ['i转换 tips 文件名翻译结果', software_utils.convert_tip_file_names],
            ['i输出名字和版本', software_utils.print_name_and_version, False],
        ]
        action_list = self.parse_action_list(action_list)

        print('当前软件状态')
        self.print_software_status(self.software_list)
        print()

        common_utils.choose_action(action_list, True)

    def parse_action_list(self, action_list: List):
        """重新解析操作列表

        以 i 开头的操作将为迭代所有软件"""
        for i, action in enumerate(action_list):
            name = action[0]
            if name.startswith('i') and len(action) > 1:  # 迭代
                # 直接 + 不使用 extend（返回 None）
                new_action = [
                    name.lstrip('i'),
                    self.iter_software,
                    action[1],
                ]
                if len(action) > 2:  # 添加额外参数
                    new_action.extend(action[2:])
                action_list[i] = new_action
        return action_list

    def iter_software(self, method: Callable, print_msg=True):
        """迭代所有软件"""
        length = len(self.software_list)
        execute_count = 0
        ignore_count = 0
        for i, software in enumerate(self.software_list):
            if not software.checked:
                ignore_count += 1
                if print_msg:
                    print(f'\n过滤 {i + 1}/{length} {software.name}')
                continue
            execute_count += 1
            if print_msg:
                print(f'\n处理 {i + 1}/{length} {software.name}')
            method(software)
        print(f'\n执行完毕，执行 {execute_count} 个，过滤 {ignore_count} 个')

    def check_software(self, software_list: List[Software]):
        """选择要操作的软件"""
        while True:
            self.print_software_status(software_list)
            index_list = self.parse_input_index(input('请输入序号选择或取消选择（0 退出，支持 1 1,2 1-2 all）\n'))
            if index_list:
                if len(index_list) == 1:
                    if index_list[0] == 0:  # 退出
                        return
                    elif index_list[0] == 'all':  # 选中全部
                        for software in software_list:
                            software.toggle_checked()
                        continue
                for index in index_list:  # 选中输入
                    if 0 < index <= len(software_list):
                        software = software_list[index - 1]
                        software.toggle_checked()

    @staticmethod
    def print_software_status(software_list: List[Software]):
        """输出软件状态"""
        for i, software in enumerate(software_list):
            print(f'{i + 1}\t' + software.get_check_status())

    @staticmethod
    def parse_input_index(text: str) -> List:
        """解析输入的 index

        >>> TranslatorX.parse_input_index('1,2 3 4-6')
        [1, 2, 3, 4, 5, 6]
        """
        if not text:
            return []
        if text.lower() == 'all':
            return ['all']
        index_list = []
        for i in text.split(' '):  # 空格分隔
            i_list = i.split(',')  # 逗号分隔
            for j in i_list:
                if '-' in j:
                    start, end = j.split('-')
                    start, end = int(start), int(end)
                    index_list.extend([int(k) for k in range(start, end + 1)])
                else:
                    index_list.append(int(j))
        return index_list


if __name__ == '__main__':
    TranslatorX().main()
