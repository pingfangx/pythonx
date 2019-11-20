from typing import List

from twisted.trial import unittest


class Solution:
    """20190829"""

    def minPathSum(self, grid: List[List[int]]) -> int:
        """
        同 0063

        1
        https://leetcode.com/problems/minimum-path-sum/discuss/23466/Simple-python-dp-70ms
        直接修改 grid
        """
        n = len(grid)
        m = len(grid[0])
        for i in range(1, m):  # 第一行
            grid[0][i] += grid[0][i - 1]
        for i in range(1, n):  # 第一列
            grid[i][0] += grid[i - 1][0]
        for i in range(1, n):
            for j in range(1, m):
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
        return grid[n - 1][m - 1]


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
