"""
数学相关
"""
import math

from study.blog.encoding import rsa


def is_prime(n: int) -> bool:
    """是否是质数

    >>> [is_prime(n) for n in [0,-1]]
    [False, False]
    >>> [is_prime(n) for n in [1,2,3,4,5]]
    [True, True, True, False, True]
    >>> [is_prime(n) for n in [6,7,8,9,10]]
    [False, True, False, False, False]
    """
    if n < 1:
        return False
    sqr = int(math.sqrt(n))
    for i in range(2, sqr + 1):
        if n % i == 0:
            return False
    return True


def is_coprime(a: int, b: int) -> bool:
    """是否是互质关系

    >>> is_coprime(2,3)
    True
    >>> is_coprime(15,32)
    True
    >>> is_coprime(7,49)
    False
    """
    return True if rsa.gcd(a, b) == 1 else False


def modular_multiplicative_inverse(e: int, phi: int):
    """求模反元素 d

    ed ≡ 1 (mod φ(n))
    即求 ed-kφ(n)=1
    即 ex+φ(n)y=1 求 x 的值
    >>> modular_multiplicative_inverse(17,3120)
    2753
    """
    x, y = rsa.extended_euclidean_algorithm(e, phi)
    while x < 0:
        # 因为扩展欧几里得算法求出的解可能为负数，推出一个正数解
        # x 增加 b/g ，y 减小 a/g
        x += phi
    return x


def encrypt(n, e, m):
    """加密

    m^e ≡ c (mod n)

    >>> encrypt(3233,17,65)
    2790
    """
    return m ** e % n


def decrypt(n, d, c):
    """解密

    c^d ≡ m (mod n)

    >>> decrypt(3233,2753,2790)
    65
    """
    return c ** d % n


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
