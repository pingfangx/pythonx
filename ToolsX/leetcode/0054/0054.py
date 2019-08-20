from typing import List

from twisted.trial import unittest


class Solution:
    """20190820"""

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """考虑用类似指针移动"""
        if not matrix or not matrix[0]:
            return []
        return self.spiral_order(matrix, 0)

    def spiral_order(self, matrix: List[List[int]], start: int) -> List[int]:
        rows = len(matrix)
        cols = len(matrix[0])
        if cols - start - start <= 0 or rows - start - start <= 0:
            return []
        ans = []
        end_col = cols - 1 - start
        end_row = rows - 1 - start
        for i in range(start, end_col + 1):  # top
            ans.append(matrix[start][i])
        for i in range(start + 1, end_row + 1):  # right,从 start+1
            ans.append(matrix[i][end_col])
        if end_row != start:  # 顶行和底行
            for i in range(end_col - 1, start - 1, -1):  # bottom，从 end-1
                ans.append(matrix[end_row][i])
        if end_col != start:  # 右列和左列
            for i in range(end_row - 1, start, -1):  # left,从 end-1 到 start
                ans.append(matrix[i][start])
        ans.extend(self.spiral_order(matrix, start + 1))
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        _output = Solution().spiralOrder(_input)
        _expect = [1, 2, 3, 6, 9, 8, 7, 4, 5]
        self.assertListEqual(_expect, _output)
