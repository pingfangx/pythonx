import logging
import os
import time


def get_logger(name):
    now = time.strftime('%Y%m%d_%H%M%S')
    file = f'log/{now}.log'
    dir_name = os.path.dirname(file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(file, encoding='utf-8')
    logger.addHandler(file_handler)
    return logger


log = get_logger('xx')
