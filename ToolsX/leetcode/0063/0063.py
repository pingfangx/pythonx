from typing import List

from twisted.trial import unittest


class Solution:
    """20190828"""

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        """
        回到 0062 的解法
        继续超时
        """
        n = len(obstacleGrid)
        m = len(obstacleGrid[0])
        dp = [[0] * m for _ in range(n)]
        for i in range(m):
            if obstacleGrid[0][i] == 0:
                dp[0][i] = 1
            else:
                break
        for i in range(n):
            if obstacleGrid[i][0] == 0:
                dp[i][0] = 1
            else:
                break
        for i in range(1, n):
            for j in range(1, m):
                if obstacleGrid[i][j] == 0:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[n - 1][m - 1]


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        _output = Solution().uniquePathsWithObstacles(_input)
        _expect = 2
        self.assertEqual(_expect, _output)
