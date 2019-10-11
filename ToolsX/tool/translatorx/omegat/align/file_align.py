from omegat.align import BaseAlign
from omegat.align.html_align import HtmlAlign


class FileAlign(BaseAlign):
    """检查文件类型"""

    def align_inner(self, source, target) -> dict:
        translation = {}
        if source.endswith('.html') and target.endswith('.html'):
            translation = HtmlAlign().align(source, target)
        else:
            print(f'暂时无法处理的文件类型\n{source}\n{target}')
        return translation
