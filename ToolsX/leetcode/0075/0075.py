from typing import List

from twisted.trial import unittest


class Solution:
    """20190905"""

    def sortColors(self, nums: List[int]) -> None:
        """
        描述中直接给了提示，可以计数，导致没有思考就用了 counter
        """
        from collections import Counter
        c = Counter(nums)
        for i in range(len(nums)):
            if i < c[0]:
                nums[i] = 0
            elif i < c[0] + c[1]:
                nums[i] = 1
            else:
                nums[i] = 2


class _Test(unittest.TestCase):
    def test(self):
        _input = [2, 0, 2, 1, 1, 0]
        Solution().sortColors(_input)
        _output = _input
        _expect = [0, 0, 1, 1, 2, 2]
        self.assertListEqual(_expect, _output)
