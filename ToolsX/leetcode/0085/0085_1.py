from typing import List

from twisted.trial import unittest


class Solution:
    """20190914"""

    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        """以我的能力，只能实现穷举

        1
        虽然说基于上一题，但是我还是没有做出来
        https://leetcode.com/problems/maximal-rectangle/discuss/29065/AC-Python-DP-solutioin-120ms-based-on-largest-rectangle-in-histogram
        """
        if not matrix or not matrix[0]:
            return 0
        n = len(matrix[0])
        height = [0] * (n + 1)  # 记录某一列的高度
        ans = 0
        for row in matrix:
            for i in range(n):
                height[i] = height[i] + 1 if row[i] == '1' else 0  # 高度+1 或置 0
            stack = [-1]
            for i in range(n + 1):
                while height[i] < height[stack[-1]]:
                    h = height[stack.pop()]
                    w = i - 1 - stack[-1]
                    ans = max(ans, h * w)
                stack.append(i)
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
