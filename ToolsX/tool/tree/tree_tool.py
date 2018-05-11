from xx import filex
from xx import iox


class TreeTool:
    def main(self):
        blogx_file = 'data/blogx.txt'
        action_list = [
            ['退出', exit],
            ['读取并显示文件', self.read_and_show, blogx_file],
        ]
        iox.choose_action(action_list)

    def read_and_show(self, file_path):
        """
        读取文件
        :param file_path: 文件路径
        :return: 
        """
        lines = filex.read_lines(file_path)
        root = self.parse_file_from_lines(lines)
        if root is not None:
            print(self.parse_file_to_text(root))

    @staticmethod
    def parse_file_from_lines(lines):
        """从行中解析为文件"""
        if not lines:
            return None

        # 使用 root 方便管理根目录多个文件的情况，返回 root.child
        root = File('root')
        root.index = 0
        pre_file = root
        for line in lines:
            current_file = File(line)
            if current_file.index > pre_file.index:
                """
                升级，增加到 child
                A
                    B
                """
                pre_file.add_child(current_file)
            elif current_file.index == pre_file.index:
                """
                同级，加到 parent.child
                """
                pre_file.parent.add_child(current_file)
            else:
                """
                降级，pre_file 降级，再添加到 parent.child
                    A
                B
                """
                dif = pre_file.index - current_file.index
                for i in range(dif):
                    pre_file = pre_file.parent
                pre_file.parent.add_child(current_file)
            # 置 pre 为 current
            pre_file = current_file
        return root

    def parse_file_to_text(self, file, pre='', is_last=True):
        """解析 file 为文本"""
        text = ''

        # 输出名字
        if file.index != 0:
            symbol = '└' if is_last else '├'
            comment = file.comment
            text += '\n%s%s─%s%s' % (pre, symbol, file.name, (',备注：' + comment if comment else ''))

        # 添加 child
        # 由一个 file 指向 child ，如果后面还有 child ，添加 | ，否则留空
        if file.index != 0:
            if is_last:
                pre += 4 * ' '
            else:
                pre += '│' + 3 * ' '
        size = len(file.child)
        for i in range(size):
            is_last = (i == size - 1)
            text += self.parse_file_to_text(file.child[i], pre, is_last)
        return text


class File:
    def __init__(self, name):
        name = name.replace(4 * ' ', '\t')
        self.index = name.count('\t') + 1
        "层级"

        name = name.strip('\n\t')
        result = name.split("'")
        self.name = result[0]
        "名字"

        if len(result) > 1:
            self.comment = result[1]
            "注释"
        else:
            self.comment = ''

        self.child = []
        self.parent = None

    def add_child(self, file):
        file.parent = self
        self.child.append(file)

    def __str__(self):
        return '%s : child %d,index %d' % (self.name, len(self.child), self.index)


if __name__ == '__main__':
    TreeTool().main()
