class Solution:
    """20190827"""

    def uniquePaths(self, m: int, n: int) -> int:
        """
        喜欢这样的题

        该解法记录了路径，如果不需要路径，可以只记录数量就可以了
        但是超时，想一想，想不出来，好像可以直接计算，但是我的思维可能还差一点
        28 的时候为 7+6+5+4+3+2+1

        1
        https://leetcode.com/problems/unique-paths/discuss/23003/1-Line-Math-Solution-(Python)
        以 3,2 为例，可以有 2 次右，1次下
        (3+2-2)!
        所有可能为
        123
        132
        213
        231
        312
        321
        将 1 2 3 分别替换为右右左
        右右左
        右左右
        右右左
        右左右
        左右右
        左右右
        需要去重，为什么去重是 (m-1)!*(n-1)!呢
        C(n,k)=P(n,k)/k!=n!/k!(n-k)!
        此时 n 为 (m-1)+(n-1)
        排列组合快忘记了

        >>> Solution().uniquePaths(3,2)
        3
        >>> Solution().uniquePaths(7,3)
        28
        """
        import math
        return math.factorial(m + n - 2) // (math.factorial(m - 1) * math.factorial(n - 1))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
