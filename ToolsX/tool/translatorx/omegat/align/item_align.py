from pathlib import Path

from omegat.align import BaseAlign
from omegat.align.dir_align import DirAlign
from omegat.align.file_align import FileAlign


class ItemAlign(BaseAlign):
    """从 IterAlign 调用，检查 item 是文件或路径"""

    def align_inner(self, source, target) -> dict:
        source = str(source)  # 提前转为 str
        target = str(target)
        translation = {}
        if Path(source).is_file() and Path(target).is_file():  # 文件
            translation = FileAlign().align(source, target)
        elif Path(source).is_dir() and Path(target).is_dir():  # 目录
            translation = DirAlign().align(source, target)
        else:
            print(f'文件目录类型不一致或不存在')
        return translation
