class Pow:
    """求幂"""

    def iter_pow(self, x, n):
        """
        迭代求幂
        直接迭代
        T(n)=O(n)

        >>> Pow().iter_pow(2,5)
        32
        """
        r = 1
        for i in range(n):
            r *= x
        return r


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
