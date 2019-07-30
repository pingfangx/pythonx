class Solution:
    """20190729"""

    def divide(self, dividend: int, divisor: int) -> int:
        """
        除，这样相减肯定超时呀，并且溢出也没有处理好
        防止溢出应该转为负数就好了

        >>> Solution().divide(10,3)
        3
        >>> Solution().divide(7,-3)
        -2
        >>> Solution().divide(-2147483648,-1)#溢出
        2147483647
        """
        if divisor == 0:
            return (2 << 31) - 1
        signum = 1
        if dividend < 0 and divisor < 0:  # 都是负
            dividend = -dividend
            divisor = -divisor
        elif dividend < 0:  # 其中一个为负
            dividend = -dividend
            signum = -1
        elif divisor < 0:
            divisor = -divisor
            signum = -1

        quotient = 0
        while dividend >= divisor:
            quotient += 1
            dividend -= divisor

        return quotient if signum == 1 else -quotient


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
