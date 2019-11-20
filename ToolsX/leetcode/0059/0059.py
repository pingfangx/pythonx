from typing import List

from twisted.trial import unittest


class Solution:
    """20190824"""

    def generateMatrix(self, n: int) -> List[List[int]]:
        """和 0054 中一样"""
        ans = [[0] * n for _ in range(n)]
        i = 1
        for row, col in self.spiral_order(n, 0):
            ans[row][col] = i
            i += 1
        return ans

    def spiral_order(self, n, start):
        if n - start - start <= 0:
            return
        end = n - 1 - start
        for i in range(start, end + 1):  # top
            yield start, i
        for i in range(start + 1, end + 1):  # right
            yield i, end
        if end != start:
            for i in range(end - 1, start - 1, -1):  # bottom
                yield end, i
            for i in range(end - 1, start, -1):  # left
                yield i, start
        for i in self.spiral_order(n, start + 1):
            yield i


class _Test(unittest.TestCase):
    def test(self):
        _input = 3
        _output = Solution().generateMatrix(_input)
        _expect = [
            [1, 2, 3],
            [8, 9, 4],
            [7, 6, 5]
        ]
        self.assertListEqual(_expect, _output)
