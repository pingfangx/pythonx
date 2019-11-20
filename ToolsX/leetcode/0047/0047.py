from typing import List

from twisted.trial import unittest


class Solution:
    """20190814"""

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        """
        在前一题的基础上去重
        去重一般就是先排序，然后配合 if i > 0 and nums[i] == nums[i - 1]: 即可
        """
        if not nums:
            return []
        ans = []
        nums.sort()
        self._permute(ans, [], nums)
        return ans

    def _permute(self, ans: List[List[int]], pre: List[int], nums: List[int]):
        if len(nums) == 0:
            ans.append(pre.copy())
        else:
            for i in range(len(nums)):
                if i > 0 and nums[i] == nums[i - 1]:
                    continue
                num = nums[i]
                pre.append(num)
                del nums[i]
                self._permute(ans, pre, nums)
                nums.insert(i, num)
                pre.pop()


class _Test(unittest.TestCase):
    def test(self):
        nums = [1, 1, 2]
        output = [
            [1, 1, 2],
            [1, 2, 1],
            [2, 1, 1]
        ]
        self.assertListEqual(Solution().permuteUnique(nums), output)
