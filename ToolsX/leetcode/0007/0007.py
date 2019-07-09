class Solution:
    def reverse(self, x: int) -> int:
        """

        要注意的是 32 位整型，如果反转可能溢出， 应该用 long 接收
        一定要注意符号，因为整除是得到 <= 商的整数，所以
        -12//10=-2
        所以
        -12%10=8
        但是在 java 里却是 -2
        >>> Solution().reverse(123)
        321
        >>> Solution().reverse(-123)
        -321
        >>> Solution().reverse(0)
        0
        >>> Solution().reverse(1)
        1
        >>> Solution().reverse(1534236469)
        0
        """
        if x < 0:
            symbol = -1
            x = -x
        else:
            symbol = 1
        r = 0
        while x:
            r *= 10
            r += x % 10
            x //= 10
        if symbol < 0:
            # 最大可取到 1<<31
            if r > 1 << 31:
                return 0
        else:
            # 最大可取到 (1<<31)-1
            if r >= 1 << 31:
                return 0
        return r * symbol


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
