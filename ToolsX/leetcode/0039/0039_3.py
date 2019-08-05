from typing import List

from twisted.trial import unittest


class Solution:
    """20190806"""

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        主要是可以使用无限次

        1
        看了讨论，使用标准回溯法

        2
        稍微优化
        """
        candidates.sort()
        ans = []
        self.combination_sum(ans, [], candidates, target, 0)
        return ans

    def combination_sum(self, ans: List[List[int]], pre: List[int], candidates: List[int], target: int,
                        start: int):
        for i in range(start, len(candidates)):
            num = candidates[i]
            if num > target:
                break
            pre.append(num)
            if num == target:
                ans.append(pre.copy())
                pre.pop()
                break
            else:
                self.combination_sum(ans, pre, candidates, target - num, i)
                pre.pop()


class _Test(unittest.TestCase):
    def test(self):
        candidates = [2, 3, 5]
        target = 8
        expect = [
            [2, 2, 2, 2],
            [2, 3, 3],
            [3, 5]
        ]
        self.assertEqual(expect, Solution().combinationSum(candidates, target))
