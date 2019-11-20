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
        if target < 0:
            return False
        elif target == 0:
            ans.append(pre.copy())
            return False
        else:
            for i in range(start, len(candidates)):
                num = candidates[i]
                pre.append(num)
                append = self.combination_sum(ans, pre, candidates, target - num, i)
                pre.pop()
                if not append:  # 因为是按顺序的，如果已经 target < 0 那么后续的依然是 target < 0
                    break
        return True


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
