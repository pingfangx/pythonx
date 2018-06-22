import pyperclip


def copy(text, print_msg=True):
    """复制到剪贴板"""
    pyperclip.copy(text)
    if print_msg:
        print(f'已复制【{text}】')
