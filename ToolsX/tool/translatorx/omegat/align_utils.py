from pathlib import Path

import translatorx_utils
from omegat.align import BaseAlign
from omegat.align.dir_align import DirAlign
from omegat.align.file_align import FileAlign
from omegat.segment import segment
from omegat.tag import shortcut_tag
from xx import iox


class AlignUtils(BaseAlign):
    name = '文件对齐工具'
    """文件对齐

    类型 Trados 的文件对齐功能，但是 Trados 的效果不是很理想，很多内容都没有对齐
    由于格式非常规整，尝试自己实现一个
    """

    def __init__(self, source, target, output=None, output_mode='a'):
        self.source = source
        self.target = target
        self.output = output
        self.output_mode = output_mode
        """输出模式 a 或 w"""

    def main(self):
        action_list = [
            ['退出', exit],
            ['对齐并处理', self.align_and_process],
        ]
        iox.choose_action(action_list)

    def align_and_process(self):
        self.align(self.source, self.target)

    def align_inner(self, source, target) -> dict:
        translation = {}
        if Path(self.source).is_file() and Path(self.target).is_file():  # 文件
            translation = FileAlign().align(self.source, self.target)
        elif Path(self.source).is_dir() and Path(self.target).is_dir():  # 目录
            translation = DirAlign().align(self.source, self.target)
        else:
            print(f'文件目录类型不一致')
        if translation:
            translation = self.process_translation(translation)
        return translation

    def process_translation(self, translation: dict):
        print(f'对齐文档共 {len(translation)} 条记录')

        translation = segment.break_translation(translation)
        print(f'分割片段共 {len(translation)} 条记录')

        translation = shortcut_tag.shortcut_tag_of_translation(translation)
        print(f'缩短标签共 {len(translation)} 条记录')

        if self.output:
            print(f'保存记忆文件')
            if self.output_mode == 'a' and Path(self.output).exists():
                t = translatorx_utils.get_translation_dict_from_omegat_file(self.output)
                translation.update(t)
                print(f'原始文件有 {len(t)} 项，添加后共 {len(translation)} 项')
            translatorx_utils.save_translation_dict_to_omegat_file(translation, self.output)
        return translation


if __name__ == '__main__':
    AlignUtils(
        source=r'D:\software\program\java\jdk1.6\java-api-1.6-en\api\java\io\package-summary.html',
        target=r'D:\software\program\java\jdk1.6\java-api-1.6-cn\api\java\io\package-summary.html',
        output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\0-Python-align.tmx'
    ).align_and_process()
