from omegat.align import BaseAlign
from omegat.align.html_align import HtmlAlign


class FileAlign(BaseAlign):
    name = '文件'
    print_info = False

    def align_inner(self, source, target) -> dict:
        translation = {}
        if source.endswith('.html') and target.endswith('.html'):
            translation = HtmlAlign().align(source, target)
        else:
            print(f'暂时无法处理的文件类型\n{source}\n{target}')
        return translation
