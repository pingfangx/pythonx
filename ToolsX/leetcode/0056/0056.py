from typing import List

from twisted.trial import unittest


class Solution:
    """20190822"""

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        先排序，然后比较前者的 [1] 和 后者的 [0] 的关系
        速度慢，是因为 pop 吗
        """
        intervals.sort()
        i = 0
        while i < len(intervals) - 1:
            if intervals[i][1] >= intervals[i + 1][0]:  # 重叠
                intervals[i][1] = max(intervals[i][1], intervals[i + 1][1])
                intervals.pop(i + 1)
            else:
                i += 1
        return intervals


class _Test(unittest.TestCase):
    def test(self):
        _input = [[1, 3], [2, 6], [8, 10], [15, 18]]
        _output = Solution().merge(_input)
        _expect = [[1, 6], [8, 10], [15, 18]]
        self.assertListEqual(_expect, _output)
