from typing import List

from twisted.trial import unittest


class Solution:
    """20190813"""

    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        一次完成，之前做过很多次了
        用 ans 保存答案，用 pre 记录之前的，执行入栈出栈操作，nums 递减
        """
        if not nums:
            return []
        ans = []
        self._permute(ans, [], nums)
        return ans

    def _permute(self, ans: List[List[int]], pre: List[int], nums: List[int]):
        if len(nums) == 0:
            ans.append(pre.copy())
        else:
            for i in range(len(nums)):
                num = nums[i]
                pre.append(num)
                del nums[i]
                self._permute(ans, pre, nums)
                nums.insert(i, num)
                pre.pop()


class _Test(unittest.TestCase):
    def test(self):
        nums = [1, 2, 3]
        output = [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1]
        ]
        self.assertListEqual(Solution().permute(nums), output)
