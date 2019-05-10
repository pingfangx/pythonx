import os


def save_file(path, text):
    """保存文件"""
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'保存完成 {path}')


def add_file_extension(file_path):
    """添加扩展名"""
    _, ext = os.path.splitext(file_path)
    if not ext or ext != '.html':
        # 如果没有扩展名，则添加
        file_path += '.html'
    return file_path
