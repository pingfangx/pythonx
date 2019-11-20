from typing import List

from twisted.trial import unittest


class Solution:
    """20190918"""

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """前一个是 0078，只需要加个排序就好了"""
        ans = []
        self.subsets(ans, sorted(nums), [], 0)
        return ans

    def subsets(self, ans: List[List[int]], nums: List[int], pre: List[int], start: int):
        ans.append(pre.copy())
        for i in range(start, len(nums)):
            if i != start and nums[i] == nums[i - 1]:
                continue
            self.subsets(ans, nums, pre + [nums[i]], i + 1)


class _Test(unittest.TestCase):
    def test(self):
        _input = [1, 2, 2]
        _output = Solution().subsetsWithDup(_input)
        _expect = [
            [2],
            [1],
            [1, 2, 2],
            [2, 2],
            [1, 2],
            []
        ]
        self.assertListEqual(sorted(_expect), sorted(_output))
