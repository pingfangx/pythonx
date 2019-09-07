from typing import List

from twisted.trial import unittest


class Solution:
    """20190907"""

    def combine(self, n: int, k: int) -> List[List[int]]:
        """从 n 里面选 k 个，但是注意是组合，不是排列

        结果慢得不行
        """
        ans = []
        self.combination(ans, [], [i + 1 for i in range(n)], k)
        return ans

    def combination(self, ans: List[List[int]], pre: List[int], nums: List[int], k: int):
        """组合"""
        if len(pre) == k:
            ans.append(pre.copy())
        else:
            for i in range(len(nums)):
                num = nums[i]
                if pre and num < pre[-1]:  # 保证 pre 中是升序的，有降序认为是重复
                    continue
                pre.append(num)
                nums.pop(i)
                self.combination(ans, pre, nums, k)
                nums.insert(i, num)
                pre.pop()

    def permutation(self, ans: List[List[int]], pre: List[int], nums: List[int], k: int):
        """排列"""
        if len(pre) == k:
            ans.append(pre.copy())
        else:
            for i in range(len(nums)):
                num = nums[i]
                pre.append(num)
                nums.pop(i)
                self.permutation(ans, pre, nums, k)
                nums.insert(i, num)
                pre.pop()


class _Test(unittest.TestCase):
    def test(self):
        _input = []
        _output = Solution().combine(4, 2)
        _expect = [
            [2, 4],
            [3, 4],
            [2, 3],
            [1, 2],
            [1, 3],
            [1, 4],
        ]
        self.assertListEqual(_expect, _output)
