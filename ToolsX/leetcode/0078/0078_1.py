from typing import List

from twisted.trial import unittest


class Solution:
    """20190908"""

    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        可以从 0 依次增加过去

        1
        https://leetcode.com/problems/subsets/discuss/27356/5-lines-of-python
        很棒的思路
        取出数字，依次加到之前的结果中
        []
        第 1 轮添加
        [1]
        第 2 轮添加
        [2], [1, 2]
        第 3 轮添加
        [3], [1, 3], [2, 3], [1, 2, 3]
        """
        ans = [[]]
        for num in nums:
            ans += [i + [num] for i in ans]
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [1, 2, 3]
        _output = Solution().subsets(_input)
        _expect = [
            [3],
            [1],
            [2],
            [1, 2, 3],
            [1, 3],
            [2, 3],
            [1, 2],
            []
        ]
        self.assertListEqual(sorted(_expect), sorted(_output))
