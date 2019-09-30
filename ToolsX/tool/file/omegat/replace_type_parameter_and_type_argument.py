from xx import filex, iox

cn_type_param = '类型参数'
cn_type_parameter = '类型形参'
cn_type_argument = '类型实参'
en_type_parameter = 'type parameter'
en_type_argument = 'type argument'


class Demo:
    """将类型参数区分为类型形参和类型实参"""

    def main(self):
        action_list = [
            ['退出', exit],
            [f'替换 {cn_type_param} 为 {cn_type_parameter} 和 {cn_type_argument}', self.replace],
            ['检查', self.check],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def replace():
        in_file = r'ignore/project_save.tmx'
        out_file = r'ignore/project_save_result.tmx'
        lines = filex.read_lines(in_file)

        sep = '=' * 10
        for i, line in enumerate(lines):
            if cn_type_param in line:
                print(f'在 {i + 1} 行找到 {cn_type_param}')
                en_line = lines[i - 3]
                en_type_parameter_count = en_line.lower().count(en_type_parameter)
                en_type_argument_count = en_line.lower().count(en_type_argument)
                if not en_type_parameter_count and not en_type_argument_count:
                    print(sep + f' 英文中没有相关单词 {en_line}' + sep)
                elif en_type_parameter_count and en_type_argument_count:
                    print(sep + f'英文中两者都有，不翻译 {en_line}' + sep)
                elif en_type_parameter_count:
                    print(f'英文中仅有 {en_type_parameter}，替换 {cn_type_param}->{cn_type_parameter}')
                    lines[i] = line.replace(cn_type_param, cn_type_parameter)
                elif en_type_argument_count:
                    print(f'英文中仅有 {en_type_argument}，替换 {cn_type_param}->{cn_type_argument}')
                    lines[i] = line.replace(cn_type_param, cn_type_argument)
                else:
                    print(sep + f'异常情况' + sep)
        filex.write_lines(out_file, lines)

    @staticmethod
    def check():
        """
        替换的时候不适合用 xml 解析，因为可能会丢字段，但检查其实是可以用解析的
        这里还是暂时用读取行
        """
        d = {
            en_type_parameter: cn_type_parameter,
            en_type_argument: cn_type_argument,
            'formal type parameter': '形式类型形参',
            'actual type argument': '实际类型实参',
        }
        in_file = r'ignore/project_save.tmx'
        lines = filex.read_lines(in_file)
        count = 0
        for i, line in enumerate(lines):
            line = line
            # 检查语言
            en = 'lang="EN-US"' in lines[i - 1]
            cn = 'lang="ZH-CN"' in lines[i - 1]
            if not en and not cn:
                continue
            # 获取中英文并转为小写
            if en:
                en_line = line.lower()
                cn_line = lines[i + 3].lower()
            else:
                en_line = lines[i - 3].lower()
                cn_line = line.lower()
            if en_line == cn_line:
                continue  # 相等不需要处理
            for en, cn in d.items():
                if en in en_line and cn not in cn_line:
                    count += 1
                    print(f'{count},第 {i + 1} 行，存在英文 {en} 却不存在中文 {cn}')
                if cn in line and en not in en_line:
                    count += 1
                    print(f'{count},第 {i + 1} 行，存在中文 {cn} 却不存在英文 {en}')


if __name__ == '__main__':
    Demo().main()
