def extended_euclidean_algorithm(a, b):
    """扩展欧几里得算法

    :return: 返回 x,y
    """
    x, y, _ = _extended_euclidean_algorithm(a, b)
    return x, y


def _extended_euclidean_algorithm(a, b):
    """扩展欧几里得算法

    ;:return 返回 x,y,q

    >>> _extended_euclidean_algorithm(47,30)
    (-7, 11, 1)
    """
    if b == 0:
        return 1, 0, a
    else:
        # q = gcd(a, b) = gcd(b, a%b)
        x, y, q = _extended_euclidean_algorithm(b, a % b)
        # 这一步是倒回去的步骤，其实不太理解，
        x, y = y, (x - (a // b) * y)
        return x, y, q


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
