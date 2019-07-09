class Solution:
    def mySqrt(self, x: int) -> int:
        """
        从 0 到 n 肯定不行，可以优化为到 n/2

        1
        只计算一次，依然超时，只好用二分的了

        >>> Solution().mySqrt(1060472158)
        32564
        """
        negative = False
        if x < 0:
            negative = True
            x = -x
        i = 0
        for i in range(x + 1):
            if i ** 2 < x:
                continue
            elif i ** 2 == x:
                break
            elif i ** 2 > x:
                i -= 1
                break
        if negative:
            return complex(0, i)
        else:
            return i


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
