class Solution:
    def mySqrt(self, x: int) -> int:
        """
        从 0 到 n 肯定不行，可以优化为到 n/2

        >>> Solution().mySqrt(4)
        32564
        """
        if x < 0:
            return None
        # 虽然是到 x 但是求出值后会返回，要注意 0 和 1，所以 +1
        for i in range(x + 1):
            if i ** 2 <= x < (i + 1) ** 2:
                # 每次都要计算两次，直接超时
                return i
        # 肯定会返回，不会执行到
        return None


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
