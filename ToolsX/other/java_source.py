import os
import shutil
from xml.etree import ElementTree as Et

from xx import filex
from xx import iox


class JavaSource:
    def main(self):
        uml_file = r'D:\workspace\DataStructureAndAlgorithm\JavaSource\src\main\resources\collections\collections2.uml'
        source_root = r'D:\xx\software\program\java\jdk\jdk1.8.0_152\src'
        target_root = r'D:\workspace\DataStructureAndAlgorithm\JavaSource\src\main\java'
        action_list = [
            ['退出', exit],
            ['根据 uml 图复制所需的 java 文件', self.copy_required_class_of_uml, uml_file, source_root, target_root],
            ['将使用系统源码的 uml 图转为使用项目中的代码', self.convert_uml, uml_file, source_root, target_root],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def convert_uml(uml_file, source_root, target_root):
        # 转换文件
        lines = filex.read_lines(uml_file)
        lines = [line.replace('java.', 'java2.') for line in lines]
        filex.write_lines(uml_file, lines)
        JavaSource.copy_required_class_of_uml(uml_file, source_root, target_root)

    @staticmethod
    def copy_required_class_of_uml(uml_file, source_root, target_root):
        """
        读取 uml 文件中所需的 java 类，从 source_root 复制到 target_root
        """
        root = Et.parse(uml_file)
        nodes = root.find('nodes')
        for node in nodes.iter('node'):
            class_name = node.text
            # 根据需要替换
            class_name = class_name.replace('java2', 'java')
            class_path = os.path.sep + class_name.replace('.', os.path.sep) + '.java'
            source_path = source_root + class_path
            target_path = target_root + class_path
            print('%s → %s' % (source_path, target_path))
            if os.path.exists(source_path):
                filex.check_and_create_dir(target_path)
                shutil.copyfile(source_path, target_path)
            else:
                print('%s 不存在' % source_path)


if __name__ == '__main__':
    JavaSource().main()
