def unicode_str_to_chinese(unicode_str):
    """
    将unicode的str转为中文
    :param unicode_str: 
    :return: 
    """
    try:
        result = unicode_str.encode().decode('unicode_escape')
    except UnicodeDecodeError:
        result = unicode_str
    return result


def chinese_to_unicode(chinese_str):
    """
    中文转为unicode
    :param chinese_str: 
    :return: 
    """
    try:
        result = chinese_str.encode('unicode_escape').decode()
    except UnicodeEncodeError:
        result = chinese_str
    return result


def md5(text: str) -> str:
    """求 md5"""
    import hashlib
    hl = hashlib.md5()
    hl.update(text.encode())
    return hl.hexdigest()
