from typing import List

from twisted.trial import unittest


class Solution:
    """20190806"""

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        主要是可以使用无限次
        """
        candidates.sort()
        return self.combination_sum(candidates, target, 0)

    def combination_sum(self, candidates: List[int], target: int, start: int) -> List[List[int]]:
        ans = []
        if target < candidates[0]:  # 小于最小值
            return ans
        for i in range(start, len(candidates)):
            num = candidates[i]
            if num == target:
                ans.append([num])
                continue
            elif num > target:
                return ans
            else:
                sub = self.combination_sum(candidates, target - num, i)  # 从 i 开始，只能再加 >= i 的
                if sub:
                    for j in sub:
                        j.insert(0, num)
                        ans.append(j)
        return ans


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
