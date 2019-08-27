class Solution:
    """20190827"""

    def uniquePaths(self, m: int, n: int) -> int:
        """
        喜欢这样的题

        该解法记录了路径，如果不需要路径，可以只记录数量就可以了
        但是超时，想一想，想不出来，好像可以直接计算，但是我的思维可能还差一点
        28 的时候为 7+6+5+4+3+2+1

        2
        https://www.geeksforgeeks.org/delannoy-number/
        考虑从最后一个位置往前推，只可能从左边或上边到达
        当 m==1 or n==1 时，只能沿一个方向到达
        >>> Solution().uniquePaths(3,2)
        3
        >>> Solution().uniquePaths(7,3)
        28
        """
        if m == 1 or n == 1:
            return 1
        else:
            return self.uniquePaths(m - 1, n) + self.uniquePaths(m, n - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
