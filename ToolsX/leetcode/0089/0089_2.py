from typing import List

from twisted.trial import unittest


class Solution:
    """20190917"""

    def grayCode(self, n: int) -> List[int]:
        """每次仅变 1 位

        00
        01
        11
        10

        经过不懈努力，终于成功了，思路一直不行啊，加油
        虽然特别慢，猜想可能是 eval 处太慢了

        1
        ans 直接保存结果，不需要最后再遍历
        还是慢

        2
        这个世界太难了，不适合我
        https://leetcode.com/problems/gray-code/discuss/29891/Share-my-solution
        """
        ans = [0]
        for i in range(n):
            for j in range(len(ans) - 1, -1, -1):
                ans.append(ans[j] | (1 << i))
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = []
        _output = Solution().grayCode(2)
        _expect = [0, 1, 3, 2]
        self.assertListEqual(_expect, _output)
