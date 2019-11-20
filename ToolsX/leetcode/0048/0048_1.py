from typing import List

from twisted.trial import unittest


class Solution:
    """20190815"""

    def rotate(self, matrix: List[List[int]]) -> None:
        """
        经过分析，每次就是四个边旋转，逐渐到中心

        考虑以下情况
        左上为 start,i
        左下为 end-i,start
        右下为 end,end-i
        右上为 start+i,end
        ----0---------
        |            |
        |            0
        0            |
        |            |
        --------0----

        1
        换为 start+i 和 end-i
        """
        self.rotate_side(matrix, 0)

    def rotate_side(self, matrix: List[List[int]], start):
        n = len(matrix)
        end = n - 1 - start
        if start >= end:
            return
        for i in range(end - start):  # 第一行最后一个不需要，是从 0 旋转过去的
            t = matrix[start][start + i]
            matrix[start][start + i] = matrix[end - i][start]  # 左上=左下
            matrix[end - i][start] = matrix[end][end - i]  # 左下=右下
            matrix[end][end - i] = matrix[start + i][end]  # 右下=右上
            matrix[start + i][end] = t  # 右上=左上
        self.rotate_side(matrix, start + 1)


class _Test(unittest.TestCase):
    def test(self):
        source = [
            [5, 1, 9, 11],
            [2, 4, 8, 10],
            [13, 3, 6, 7],
            [15, 14, 12, 16]
        ]
        Solution().rotate(source)
        result = [
            [15, 13, 2, 5],
            [14, 3, 4, 1],
            [12, 6, 8, 9],
            [16, 7, 10, 11]
        ]
        self.assertListEqual(result, source)
