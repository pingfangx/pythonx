from typing import List

from twisted.trial import unittest


class Solution:
    """20190824"""

    def generateMatrix(self, n: int) -> List[List[int]]:
        """和 0054 中一样

        1
        https://leetcode.com/problems/spiral-matrix-ii/discuss/22282/4-9-lines-Python-solutions
        di,dj=dj,-di
        顶，初始为 0,1, i 不变，j 递增
        右，变换为 1,0, i 递增，j 不变
        底，0,-1
        左，-1,0

        if ans[(i + di) % n][(j + dj) % n]
        用于到最后一个元素，或者下一个元素不为空，则换方向


        """
        ans = [[0] * n for _ in range(n)]
        i = j = 0
        di, dj = 0, 1
        for k in range(n * n):
            ans[i][j] = k + 1
            if ans[(i + di) % n][(j + dj) % n]:
                di, dj = dj, -di
            i += di
            j += dj
        return ans


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
