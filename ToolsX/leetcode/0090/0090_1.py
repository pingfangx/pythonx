from typing import List

from twisted.trial import unittest


class Solution:
    """20190918"""

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """前一个是 0078，只需要加个排序就好了

        1 还是和 0078_1 一样的思路，但是需要判断是否存在
        """
        ans = [[]]
        for num in sorted(nums):
            ans += [i + [num] for i in ans if i + [num] not in ans]
        return ans


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
