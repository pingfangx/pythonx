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
        """
        ans = []
        self.gray_code(ans, [0] * n, 0, n - 1, n - 1)
        return ans

    def gray_code(self, ans, bits, left, right, i):
        if left > right:
            num = 0
            for i, bit in enumerate(bits):
                if bit:
                    num |= 1 << (right - i)
            ans.append(num)
        else:
            self.gray_code(ans, bits, left + 1, right, right)
            bits[left] ^= 1
            self.gray_code(ans, bits, left + 1, right, right)


class _Test(unittest.TestCase):
    def test(self):
        _input = []
        _output = Solution().grayCode(2)
        _expect = [0, 1, 3, 2]
        self.assertListEqual(_expect, _output)
