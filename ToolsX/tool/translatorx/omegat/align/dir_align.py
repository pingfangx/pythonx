from pathlib import Path

from twisted.trial import unittest

from omegat.align import BaseAlign
from omegat.align.file_align import FileAlign


class DirAlign(BaseAlign):
    name = '目录'
    print_info = True

    def align_inner(self, source, target) -> dict:
        source_dir = Path(source)
        target_dir = Path(target)
        translation = {}
        source_files = list(source_dir.rglob('*'))
        n = len(source_files)
        for i, source_file in enumerate(source_files):
            print(f'处理第 {i + 1}/{n} 个文件 {source_file}')
            if source_file.is_file():
                rel_path = source_file.relative_to(source_dir)
                target_file = target_dir / rel_path
                if target_file.is_file():
                    t = FileAlign().align(str(source_file), str(target_file))
                    if t:
                        translation.update(t)
        return translation


class _Test(unittest.TestCase):
    def test(self):
        translation = DirAlign().align(
            source=r'D:\xx\software\program\java\jdk1.6\java-api-1.6-en\api\java\lang',
            target=r'D:\xx\software\program\java\jdk1.6\java-api-1.6-cn\api\java\lang'
        )
        print(translation)
