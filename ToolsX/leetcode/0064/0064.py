from typing import List

from twisted.trial import unittest


class Solution:
    """20190829"""

    def minPathSum(self, grid: List[List[int]]) -> int:
        """同 0063"""
        n = len(grid)
        m = len(grid[0])
        dp = [[0] * m for _ in range(n)]
        dp[0][0] = grid[0][0]
        for i in range(1, m):  # 第一行
            dp[0][i] = dp[0][i - 1] + grid[0][i]
        for i in range(1, n):  # 第一列
            dp[i][0] = dp[i - 1][0] + grid[i][0]
        for i in range(1, n):
            for j in range(1, m):
                dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
        return dp[n - 1][m - 1]


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1]
        ]
        _output = Solution().minPathSum(_input)
        _expect = 7
        self.assertEqual(_expect, _output)
