class Solution:
    """20190827"""

    def uniquePaths(self, m: int, n: int) -> int:
        """
        喜欢这样的题

        该解法记录了路径，如果不需要路径，可以只记录数量就可以了
        但是超时，想一想，想不出来，好像可以直接计算，但是我的思维可能还差一点
        28 的时候为 7+6+5+4+3+2+1

        3
        能理解，也不超时的解法
        https://leetcode.com/problems/unique-paths/discuss/22954/C%2B%2B-DP
        >>> Solution().uniquePaths(3,2)
        3
        >>> Solution().uniquePaths(7,3)
        28
        """
        # 将 m 视为行数
        dp = [[1] * n for _ in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[m - 1][n - 1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
