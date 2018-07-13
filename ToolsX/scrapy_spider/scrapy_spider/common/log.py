import logging
import os
import time


def get_logger(name):
    now = time.strftime('%Y%m%d/%H%M%S')
    root_dir = r'D:\workspace\PythonX\ToolsX\scrapy_spider'
    file = f'{root_dir}/log/{now}.log'
    dir_name = os.path.dirname(file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(file, encoding='utf-8')

    fmt = '%(asctime)s [%(name)s] %(levelname)s: %(message)s [%(filename)s:%(lineno)s]'
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


log = get_logger('xx')
