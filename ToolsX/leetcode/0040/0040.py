from typing import List

from twisted.trial import unittest


class Solution:
    """20190807"""

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()  # 提前排序
        ans = []
        pre = []
        self.combination_sum(ans, pre, candidates, target, 0)
        return ans

    def combination_sum(self, ans: List[List[int]], pre: List[int], candidates: List[int], target: int, start):
        n = len(candidates)
        for i in range(start, n):  # 用 start 作为起点，不需要截取子数组
            if i > start and candidates[i] == candidates[i - 1]:  # == start 是可以的，因为都属于 candidates，但是如果 > 则在该循环中重复
                continue
            num = candidates[i]
            if target < num:
                return
            elif target == num:
                t = pre.copy()
                t.append(num)
                ans.append(t)
                return  # 不需要再继续循环，后续要么相同，要么大于
            else:
                pre.append(num)
                self.combination_sum(ans, pre, candidates, target - num, i + 1)  # target 减小， i+1
                pre.pop()


class _Test(unittest.TestCase):
    def test(self):
        candidates = [3, 1, 3, 5, 1, 1]
        target = 8
        expect = [[1, 1, 1, 5], [1, 1, 3, 3], [3, 5]]
        self.assertEqual(expect, Solution().combinationSum2(candidates, target))
