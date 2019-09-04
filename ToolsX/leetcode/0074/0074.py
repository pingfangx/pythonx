from typing import List

from twisted.trial import unittest


class Solution:
    """20190904"""

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """就二分吧"""
        if not matrix or not matrix[0]:
            return False
        n = len(matrix)
        m = len(matrix[0])
        left = 0
        right = n * m - 1
        while left <= right:
            mid = left + (right - left) // 2
            row, col = divmod(mid, m)
            num = matrix[row][col]
            if target == num:
                return True
            elif target < num:
                right -= 1
            else:
                left += 1
        return False


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            [1, 3, 5, 7],
            [10, 11, 16, 20],
            [23, 30, 34, 50]
        ]
        _output = Solution().searchMatrix(_input, 3)
        _expect = True
        self.assertEqual(_expect, _output)
