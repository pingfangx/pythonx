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
        """
        if n == 0:  # 因为 [0]*0 为 [] 所以特殊处理
            return [0]
        bits_array = []
        self.gray_code(bits_array, [0] * n, 0, n - 1, n - 1)
        print(bits_array)

        ans = []
        for bits in bits_array:
            ans.append(eval('0b' + ''.join([str(i) for i in bits])))
        return ans

    def gray_code(self, ans, bits, left, right, i):
        if left > right:
            ans.append(bits.copy())
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
