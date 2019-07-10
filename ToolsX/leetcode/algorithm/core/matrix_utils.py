"""
矩阵运算，可以使用 numpy
不过还是简单实现一下
"""
from typing import List


def add(a: List[List], b: List[List], sub=False) -> List[List]:
    """
    矩阵相加
    按位置相加

    >>> a=[[1,3],[1,0],[1,2]]
    >>> b=[[0,0],[7,5],[2,1]]
    >>> add(a,b)
    [[1, 3], [8, 5], [3, 3]]
    >>> subtract(a,b)
    [[1, 3], [-6, -5], [-1, 1]]
    """
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    if rows_a != rows_b:
        raise ValueError(f'rows_a={rows_a},rows_b={rows_b}')

    if cols_a != cols_b:
        raise ValueError(f'cols_a={cols_a},cols_b={cols_b}')

    _sum = [[0] * cols_a for _ in range(rows_a)]
    symbol = 1 if not sub else -1
    for i in range(rows_a):
        for j in range(cols_b):
            _sum[i][j] = a[i][j] + symbol * b[i][j]
    return _sum


plus = add


def subtract(a: List[List], b: List[List]) -> List[List]:
    """
    矩阵相减
    按位置相减
    """
    difference = add(a, b, True)
    return difference


minus = subtract


def multiply(a: List[List], b: List[List]) -> List[List]:
    """
    矩阵相乘
    设 A 是 n × m 的矩阵，B 是 m × p 的矩阵，则它们的矩阵积 AB 是 n × p 的矩阵。
    A 中每一行的 m 个元素都与 B 中对应列的 m 个元素对应相乘，这些乘积的和就是 AB 中的一个元素。
    A 中第 i 行的 0,m 乘以 B 中第 j 列的 0,p 得到元素 [i][j]

    >>> a=[[1,0,2],[-1,3,1]]
    >>> b=[[3,1],[2,1],[1,0]]
    >>> multiply(a,b)
    [[5, 1], [4, 2]]
    """
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    if cols_a != rows_b:
        raise ValueError(f'cols_a={cols_a},rows_b={rows_b}')

    # rows_a 行 cols_b 列
    product = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):  # 行
        for j in range(cols_b):  # 列
            for k in range(cols_a):
                # i 行从 0 到 k，乘上 j 列的 0 到 k
                product[i][j] += a[i][k] * b[k][j]
    return product


def power(a: List[List], n: int) -> List[List]:
    """
    矩阵幂
    >>> a=[[2,2],[2,2]]
    >>> power(a,2)
    [[8, 8], [8, 8]]
    >>> power(a,3)
    [[32, 32], [32, 32]]
    """
    rows_a = len(a)
    cols_a = len(a[0])
    _power = [[1 if i == j else 0 for j in range(rows_a)] for i in range(rows_a)]  # 对象线初始化为 1
    t = a.copy()
    while n:
        if n & 1 == 1:
            # 奇数，乘到结果上
            _power = multiply(_power, t)
        t = multiply(t, t)  # 不断平方
        n >>= 1
    return _power


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
