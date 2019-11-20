from typing import List

from twisted.trial import unittest


class Solution:
    """20190907"""

    def combine(self, n: int, k: int) -> List[List[int]]:
        """从 n 里面选 k 个，但是注意是组合，不是排列

        结果慢得不行
        1 只需要序号就可以了

        还是慢
        https://leetcode.com/problems/combinations/discuss/27024/1-liner-3-liner-4-liner
        看了别人的解法，不想做了，放弃
        """
        ans = []
        self.combination(ans, [], 1, n, k)
        return ans

    def combination(self, ans: List[List[int]], pre: List[int], start: int, n: int, k: int):
        """组合"""
        if len(pre) == k:
            ans.append(pre.copy())
        else:
            for i in range(start, n + 1):
                pre.append(i)
                self.combination(ans, pre, i + 1, n, k)
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
