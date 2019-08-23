from typing import List

from twisted.trial import unittest


class Solution:
    """20190823"""

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """
        hard 难度，有一点不想做了
        较难的题，就像是数学的大题，为了出题而出题，做出来的成就感没有解决实际问题的那种成就感

        还是按照 0056-1 中的解法，用 ans 保存，依次填入
        """
        if not intervals:
            return [newInterval]
        if not newInterval:
            return intervals

        intervals.sort()

        add_interval = False
        ans = []
        for interval in intervals:
            if not ans or not add_interval:  # 为空，或者还没有添加，都需要进行
                if interval[0] > newInterval[1]:  # 大于 newInterval 需要先插入 newInterval
                    add_interval = True
                    ans.append(newInterval)
                    ans.append(interval)
                elif interval[1] < newInterval[0]:
                    ans.append(interval)
                else:
                    add_interval = True
                    ans.append([min(interval[0], newInterval[0]), max(interval[1], newInterval[1])])
            else:  # 不为空，并且已添加，只需要和最后一个比较
                if interval[0] > ans[-1][1]:  # 最小的都比最大的大，不重叠，直接插入
                    ans.append(interval)
                else:
                    ans[-1] = [min(ans[-1][0], interval[0]), max(ans[- 1][1], interval[1])]
        if not add_interval:
            ans.append(newInterval)
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [[1, 5]]
        _output = Solution().insert(_input, [6, 8])
        _expect = [4, 8]
        self.assertListEqual(_expect, _output)

        _input = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
        _output = Solution().insert(_input, [4, 8])
        _expect = [[1, 2], [3, 10], [12, 16]]
        self.assertListEqual(_expect, _output)
