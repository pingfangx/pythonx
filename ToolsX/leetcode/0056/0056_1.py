from typing import List

from twisted.trial import unittest


class Solution:
    """20190822"""

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        先排序，然后比较前者的 [1] 和 后者的 [0] 的关系
        速度慢，是因为 pop 吗

        1 不修改 intervals ，改用 ans 保存结果
        """
        intervals.sort()
        ans = []
        for interval in intervals:
            if not ans or ans[-1][1] < interval[0]:
                ans.append(interval)
            else:  # 重叠
                ans[-1][1] = max(ans[-1][1], interval[1])
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [[1, 3], [2, 6], [8, 10], [15, 18]]
        _output = Solution().merge(_input)
        _expect = [[1, 6], [8, 10], [15, 18]]
        self.assertListEqual(_expect, _output)
