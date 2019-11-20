from typing import List

from twisted.trial import unittest


class Solution:
    """20190905"""

    def sortColors(self, nums: List[int]) -> None:
        """
        描述中直接给了提示，可以计数，导致没有思考就用了 counter

        1
        尝试一轮
        """
        left = 0
        right = len(nums) - 1
        i = left
        while i <= right:
            num = nums[i]
            if num == 2:  # 交换右边
                nums[i], nums[right] = nums[right], nums[i]
                right -= 1  # 仅 right - 1，i 不变
            elif num == 0:  # 交换左边
                nums[i], nums[left] = nums[left], nums[i]
                left += 1  # i 和 left 同时加 1
                i += 1
            else:
                i += 1


class _Test(unittest.TestCase):
    def test(self):
        _input = [2, 0, 1]
        Solution().sortColors(_input)
        _output = _input
        _expect = [0, 0, 1, 1, 2, 2]
        self.assertListEqual(_expect, _output)
