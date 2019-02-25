import os
import re

from xx import excelx
from xx import filex
from xx import iox


class UpdateRecyclerView:
    def __init__(self):
        self.work_space = r'E:\xx\work\yunyang\codes\llb-develop\app\src\main'
        self.rv_xml_files_path = r'ignore/rv_xml_files.txt'
        self.rv_java_files_path = r'ignore/rv_java_files.txt'
        self.item_xml_files_path = r'ignore/item_xml_files.txt'
        self.modified_xml_files_path = r'ignore/modified_xml_files.txt'
        self.excel_path = r'ignore/result.xls'

    def main(self):
        action_list = [
            ['退出', exit],
            ['①检查所有包含 RecyclerView 的 xml 文件', self.check_rv_xml_files],
            ['检查使用 RecyclerView 的 java 文件', self.check_rv_java_files],
            ['检查所有的 adapter 文件', self.check_adapter_files],
            ['②合并检查上两个', self.check_rv_java_and_adapter_files],
            ['③检查所使用的资源文件', self.check_use_layout_res],
            ['④修改所使用的资源文件', self.modify_use_layout_res],
            ['导出为 excel', self.export_excel],
        ]
        iox.choose_action(action_list)

    def check_rv_xml_files(self):
        files = filex.list_file(self.work_space, 'xml$')
        length = len(files)
        print('共有文件 %d 个' % length)

        rv_xml_files = []
        for i in range(length):
            file = files[i]
            print('%d/%d %s' % (i + 1, length, file))
            # 检查文件中是否包含 recycler view
            if 'RecyclerView' in filex.read(file):
                rv_xml_files.append(file)
        print('共有 %d 个文件包含 recycler view' % len(rv_xml_files))
        filex.write_lines(self.rv_xml_files_path, rv_xml_files, add_line_separator=True)

    def check_rv_java_files(self):
        """检查包含使用了包含 recycler 的 xml 文件的 java 文件"""
        rv_xml_files = filex.read_lines(self.rv_xml_files_path, ignore_line_separator=True)
        rv_xml_files = [os.path.split(file)[1].replace('.xml', '') for file in rv_xml_files]
        print('共有 %d 个 xml 文件包含 recycler view' % len(rv_xml_files))
        print(rv_xml_files)
        java_files = filex.list_file(self.work_space, 'java$')
        java_file_length = len(java_files)
        print('共有 %d 个 java 文件' % len(java_files))

        print('检查使用了资源文件的类')
        rv_java_files = []
        for i in range(java_file_length):
            java_file = java_files[i]
            # print('%d/%d %s' % (i + 1, java_file_length, java_file))
            if self.check_java_file(java_file, rv_xml_files):
                rv_java_files.append(java_file)
        print('共有 %d 个 java 文件使用了资源文件' % len(rv_java_files))

        print('添加子类')
        self.check_subclass(java_files, rv_java_files)
        return rv_java_files

    @staticmethod
    def check_java_file(java_file, rv_xml_files):
        content = filex.read(java_file)
        for file in rv_xml_files:
            layout = 'R.layout.' + file
            if layout in content:
                print('%s 使用了资源文件 %s' % (java_file, file))
                return True
        return False

    def check_subclass(self, all_file_list, result_file_list):
        """检查子类"""
        children_file_list = []
        for file in all_file_list:
            if file not in result_file_list:
                content = filex.read(file)
                # 这里可以优化为，只检查新添加的 children 中的文件，而不需要全部再检查
                for result_file in result_file_list:
                    name = os.path.splitext(os.path.split(result_file)[1])[0]
                    if 'extends ' + name in content:
                        print('%s 继承了 %s' % (file, name))
                        children_file_list.append(file)
                        break
        print('共找到 %d 个子类' % (len(children_file_list)))
        if len(children_file_list) > 0:
            # 找到子类，继续
            result_file_list.extend(children_file_list)
            print('当前大小 %d' % len(result_file_list))
            self.check_subclass(all_file_list, result_file_list)

    def check_adapter_files(self):
        """检查 adapter """
        java_file_list = filex.list_file(self.work_space, 'java$')
        print('共有 %d 个 java 文件' % len(java_file_list))
        adapter_file_list = []
        for java_file in java_file_list:
            name = 'RecyclerView.Adapter'
            if 'extends ' + name in filex.read(java_file):
                print('%s 继承了 %s' % (java_file, name))
                adapter_file_list.append(java_file)
        self.check_subclass(java_file_list, adapter_file_list)
        return adapter_file_list

    def check_rv_java_and_adapter_files(self):
        file_list1 = self.check_rv_java_files()
        file_list2 = self.check_adapter_files()
        print('大小分别为 %d,%d' % (len(file_list1), len(file_list2)))
        for file in file_list2:
            if file not in file_list1:
                file_list1.append(file)
        print('合并为 %d' % len(file_list1))
        filex.write_lines(self.rv_java_files_path, file_list1, add_line_separator=True)

    def check_use_layout_res(self):
        """根据检查出的 java 文件检查使用的布局资源"""
        java_files = filex.read_lines(self.rv_java_files_path, ignore_line_separator=True)
        pattern = re.compile(r'(?<!setContentView\()R\.layout\.(.*?)[;),]')
        name_pattern = re.compile(r'^(?!fragment|dialog|high|pop|layout|address)')
        xml_name_list = []
        for file in java_files:
            content = filex.read(file)
            all_match = re.findall(pattern, content)
            if all_match:
                print('%s 找到布局使用' % file)
                for match in all_match:
                    if re.search(name_pattern, match):
                        print(match)
                        if 'item' not in match:
                            print('不包含 item')
                        if match not in xml_name_list:
                            xml_name_list.append(match)
                    else:
                        print('过滤', match)
        print('共使用了 %d 个文件' % len(xml_name_list))
        print('查找对应的 xml 文件')
        files = filex.list_file(self.work_space, 'xml$')
        xml_file_list = []
        for xml_name in xml_name_list:
            for file in files:
                name = os.path.splitext(os.path.split(file)[1])[0]
                if xml_name == name:
                    xml_file_list.append(file)
                    break
        print('共找到 %d 个文件' % len(xml_file_list))
        filex.write_lines(self.item_xml_files_path, xml_file_list, add_line_separator=True)

    def modify_use_layout_res(self):
        """修改所使用的资源文件"""
        item_xml_files = filex.read_lines(self.item_xml_files_path, ignore_line_separator=True)
        modified_xml_files = []
        for item_xml_file in item_xml_files:
            print('检查', item_xml_file)
            if self.modify_xml_file(item_xml_file):
                modified_xml_files.append(item_xml_file)
        print('共修改 %d 个 xml 文件' % len(modified_xml_files))
        filex.write_lines(self.modified_xml_files_path, modified_xml_files, add_line_separator=True)

    @staticmethod
    def modify_xml_file(item_xml_file):
        lines = filex.read_lines(item_xml_file)
        modified = False
        length = len(lines)
        wrap_content = 'wrap_content'
        match_parent = 'match_parent'
        fill_parent = 'fill_parent'
        for i in range(length):
            line = lines[i]
            # print(line)
            if '?>' in line:
                # 第一行不处理
                continue
            if 'android:layout_width' in line:
                if wrap_content in line:
                    modified = True
                    print('layout_width 设置为 %s，改为 %s' % (wrap_content, match_parent))
                    lines[i] = line.replace(wrap_content, match_parent)
            if 'android:layout_height' in line:
                if match_parent in line:
                    modified = True
                    print('layout_height 设置为 %s，改为 %s' % (match_parent, wrap_content))
                    lines[i] = line.replace(match_parent, wrap_content)
                elif fill_parent in line:
                    modified = True
                    print('layout_height 设置为 %s，改为 %s' % (fill_parent, wrap_content))
                    lines[i] = line.replace(fill_parent, wrap_content)
            if '>' in line:
                # 标签结束
                break
        if modified:
            print('作出了修改，需要保存')
            filex.write_lines(item_xml_file, lines)
            return True
        return False

    def export_excel(self):
        """导出 excel"""
        data = []
        list1 = filex.read_lines(self.rv_java_files_path, ignore_line_separator=True)
        list2 = filex.read_lines(self.modified_xml_files_path, ignore_line_separator=True)
        list3 = filex.read_lines(self.item_xml_files_path, ignore_line_separator=True)
        list1.sort()
        list2.sort()
        list3.sort()
        title = ["是否修改", "是否已检查", "使用场景", "文件名", "文件名"]
        for file in list1:
            short_name = os.path.splitext(os.path.split(file)[1])[0]
            comment = self.read_file_comment(file)
            data.append(['', '', comment, short_name, file])
        for file in list2:
            short_name = os.path.splitext(os.path.split(file)[1])[0]
            data.append([1, '', '', short_name, file])
        for file in list3:
            # 不需要重复
            if file not in list2:
                short_name = os.path.splitext(os.path.split(file)[1])[0]
                data.append(['', '', '', short_name, file])
        excelx.write_list_to_excel(self.excel_path, data, title)

    @staticmethod
    def read_file_comment(file):
        """读取文件的注释"""
        lines = filex.read_lines(file, ignore_line_separator=True)
        length = len(lines)
        for i in range(length):
            line = lines[i]
            if 'class' in line:
                print('读取到 class')
                break
            if '/*' in line:
                comment = lines[i + 1]
                comment = comment.strip(' *')
                # print('读取到注释', comment)
                return comment
        print('没有读取到内容')
        return ''


if __name__ == '__main__':
    UpdateRecyclerView().main()
