from typing import List

from twisted.trial import unittest


class Solution:
    """20190908"""

    def subsets(self, nums: List[int]) -> List[List[int]]:
        """可以从 0 依次增加过去"""
        ans = []
        self.get_subset(ans, nums, [], 0)
        return ans

    def get_subset(self, ans: List[List[int]], nums: List[int], pre: List[int], start: int):
        ans.append(pre.copy())
        for i in range(start, len(nums)):
            if i != start and nums[i] == nums[i - 1]:
                continue
            self.get_subset(ans, nums, pre + [nums[i]], i + 1)  # pre 加上数字，同时 i 加 1


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
