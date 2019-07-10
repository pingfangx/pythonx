"""
二进制有关的工具
"""


def to_split_binary(x):
    return split_num(x)


def split_num(x: int, bits: int = 8) -> str:
    """
    >>> split_num(1<<31)
    '0b 10000000 00000000 00000000 00000000'
    """
    return split_str(bin(x), bits)


def split_str(x: str, bits: int = 8) -> str:
    """
    按位分割字符串
    :param x: 字符串
    :param bits: 分割位数
    >>> split_str('0b1000000000')
    '0b 00000010 00000000'
    """
    pre = ''
    if x.startswith('0b'):
        pre = x[0:2]
        x = x[2:]
    t = ''
    while x:
        if t:
            t = ' ' + t
        t = x[-8:].zfill(bits) + t
        x = x[:-8]
    if pre:
        t = pre + ' ' + t
    return t


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
