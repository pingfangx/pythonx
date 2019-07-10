from leetcode.algorithm.core import matrix_utils


class Pow:
    """求幂"""

    def matrix_pow(self, x, n):
        """矩阵求幂"""
        matrix_utils.power(x, n)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
