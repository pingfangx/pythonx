from pathlib import Path

import translatorx_utils
from omegat.align import BaseAlign
from omegat.align.iter_align import IterAlign
from omegat.process import process
from omegat.segment import segment
from xx import iox


class ProcessAlign(BaseAlign):
    name = '对齐并且处理'
    print_info = True
    """文件对齐

    类型 Trados 的文件对齐功能，但是 Trados 的效果不是很理想，很多内容都没有对齐
    由于格式非常规整，尝试自己实现一个
    """

    def __init__(self, source, target, output=None, output_mode='a', files=None):
        self.output = output
        self.output_mode = output_mode
        """输出模式 a 或 w"""

        if isinstance(files, list) and isinstance(source, str) and isinstance(target, str):
            self.source = [str(Path(source) / i) for i in files]
            self.target = [str(Path(target) / i) for i in files]
        else:
            self.source = source
            self.target = target

    def main(self):
        action_list = [
            ['退出', exit],
            ['对齐并处理', self.align_and_process],
        ]
        iox.choose_action(action_list)

    def align_and_process(self):
        return self.align(self.source, self.target)

    def align_inner(self, source, target) -> dict:
        translation = IterAlign().align(self.source, self.target)
        if translation:
            translation = self.process_translation(translation)
        return translation

    def process_translation(self, translation: dict):
        print(f'对齐文档共 {len(translation)} 条记录')

        # 先按换行分割，再缩短标签，再分割片段
        translation = segment.break_translation_by_lf(translation)
        print(f'按换行分割共 {len(translation)} 条记录')

        translation = process.shortcut_tag_of_translation(translation)
        print(f'缩短标签共 {len(translation)} 条记录')

        translation = segment.break_translation(translation)
        print(f'分割片段共 {len(translation)} 条记录')

        translation = process.process_of_translation(translation, lambda x: x.strip())

        translation = process.filter_incorrect_translation(translation)
        print(f'过滤不正确的翻译，共 {len(translation)} 条记录')

        if self.output:
            print(f'保存记忆文件')
            if self.output_mode == 'a' and Path(self.output).exists():
                t = translatorx_utils.get_translation_dict_from_omegat_file(self.output)
                translation.update(t)
                print(f'原始文件有 {len(t)} 项，添加后共 {len(translation)} 项')
            translatorx_utils.save_translation_dict_to_omegat_file(translation, self.output)
        return translation


if __name__ == '__main__':
    ProcessAlign(
        source=r'D:\software\program\java\jdk1.6.0_45\en改\docs\api\java',
        target=r'D:\software\program\java\jdk1.6.0_45\cn\docs\api\java',
        files=[
            r'util\HashMap.html',
        ],
        output=r'D:\workspace\TranslatorX-other\JavaDocs\tm\0-Python-align-util.tmx'
    ).align_and_process()
