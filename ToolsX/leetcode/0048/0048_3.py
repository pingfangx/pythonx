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

        2
        直接等

        3
        clockwise rotate
        first reverse up to down, then swap the symmetry
        1 2 3     7 8 9     7 4 1
        4 5 6  => 4 5 6  => 8 5 2
        7 8 9     1 2 3     9 6 3

        从下往上看，741，实际就相当于是旋转后从左往右看
        所以就有了解法，先上下颠倒，然后旋转
        上下颠倒用 [::-1]
        * 转为可迭代对象
        旋转用 zip
        结果为 tuple，所以运用 map 转为 list
        最后赋值回 matrix

        但是好像分配额外的空间了

        """
        # matrix[:] = zip(*matrix[::-1])
        matrix[:] = map(list, zip(*matrix[::-1]))


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
