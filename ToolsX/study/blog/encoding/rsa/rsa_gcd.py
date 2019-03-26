"""最大公约数相关"""
from typing import List


def _get_test_case() -> List:
    return [
        [1, 1, 1],
        [15, 20, 5],
        [100, 65, 5],
    ]


def _gcd_base(a: int, b: int) -> int:
    """求最大公约数最基本的方法

    >>> [_gcd_base(a,b)==c for a,b,c in _get_test_case()].count(False)
    0
    """
    if a == 1 or b == 1:
        return 1
    r = a % b
    while r != 0:
        a = b
        b = r
        r = a % b
    return b


def _gcd_simple(a, b):
    """简化书写

    >>> [_gcd_simple(a,b)==c for a,b,c in _get_test_case()].count(False)
    0
    """
    r = a % b
    while r:
        a, b, r = b, r, b % r
    return b


def _gcd_simple_2(a, b):
    """简化书写

    >>> [_gcd_simple_2(a,b)==c for a,b,c in _get_test_case()].count(False)
    0
    """
    while b:
        a, b = b, a % b
    return a


def _gcd_recursion(a, b):
    """递归

    >>> [_gcd_recursion(a,b)==c for a,b,c in _get_test_case()].count(False)
    0
    """
    r = a % b
    if r:
        return _gcd_recursion(b, r)
    else:
        return b


def _gcd_recursion_simple(a, b):
    """递归简化

    >>> [_gcd_recursion_simple(a,b)==c for a,b,c in _get_test_case()].count(False)
    0
    """
    return _gcd_recursion(b, a % b) if a % b else b


def gcd(a: int, b: int) -> int:
    return _gcd_simple_2(a, b)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
