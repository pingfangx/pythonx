from typing import List

from twisted.trial import unittest


class Solution:
    """20190903"""

    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        类似于之前的数独
        很空易想到时的就是在置 0 的过程中会有重复项
        最简单的方法就是循环一遍收集信息

        解答中的 O(1) 的空间复杂度
        """
        if not matrix or not matrix[0]:
            return
        n = len(matrix)
        m = len(matrix[0])

        rows = {}
        cols = {}
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 0:
                    rows[i] = ''
                    cols[j] = ''
        for row in rows.keys():
            for j in range(m):
                matrix[row][j] = 0
        for col in cols.keys():
            for i in range(n):
                matrix[i][col] = 0


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            [0, 1, 2, 0],
            [3, 4, 5, 2],
            [1, 3, 1, 5]
        ]
        Solution().setZeroes(_input)
        _output = _input
        _expect = [
            [0, 0, 0, 0],
            [0, 4, 5, 0],
            [0, 3, 1, 0]
        ]
        self.assertListEqual(_expect, _output)
