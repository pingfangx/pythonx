from typing import List

from twisted.trial import unittest


class Solution:
    """20190914"""

    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        """以我的能力，只能实现穷举"""
        if not matrix or not matrix[0]:
            return 0
        n = len(matrix)
        m = len(matrix[0])
        ans = 0
        for i in range(n):
            for j in range(m):
                num = matrix[i][j]
                if num == "1":
                    ans = max(ans, self.max_rectangle(matrix, i, j, n, m))
        return ans

    def max_rectangle(self, matrix, start_i, start_j, n, m):
        """以 i,j 为左上角，求最大矩形"""
        ans = 0
        for i in range(start_i, n):  # 向下移
            ans = max(ans, self.max_rectangle_right(matrix, start_i, i, start_j, n, m))
        return ans

    def max_rectangle_right(self, matrix, start_i, end_i, start_j, n, m):
        """向右移"""
        ans = 0
        for j in range(start_j, m):
            find = False
            for i in range(start_i, end_i + 1):
                if matrix[i][j] == '0':  # 发现0
                    find = True
                    break
            if find:
                break
            ans = (end_i - start_i + 1) * (j - start_j + 1)
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            ["1", "0", "1", "0", "0"],
            ["1", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1"],
            ["1", "0", "0", "1", "0"]
        ]
        _output = Solution().maximalRectangle(_input)
        _expect = 6
        self.assertEqual(_expect, _output)
