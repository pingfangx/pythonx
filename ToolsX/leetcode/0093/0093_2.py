from typing import List

from twisted.trial import unittest


class Solution:
    """20190921"""

    def restoreIpAddresses(self, s: str) -> List[str]:
        """
        思路，因为是 4 部分，取出一个数字做为第一部分，然后再判断后面的
        要注意范围是 0-255
        要注意不能以 0 开头

        1
        可以再优化

        2
        看了讨论，用 section 表示，我是用 n
        大家一般从 0 开始递增，我这里从 4 递减了
        然后就是这个泥石流
        https://leetcode.com/problems/restore-ip-addresses/discuss/30972/WHO-CAN-BEAT-THIS-CODE
        """
        ans = []
        n = len(s)
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(1, 4):
                    for d in range(1, 4):
                        if a + b + c + d == n:
                            A = s[:a]
                            B = s[a:a + b]
                            C = s[a + b:a + b + c]
                            D = s[a + b + c:]
                            if self.is_valid_part(A) \
                                    and self.is_valid_part(B) \
                                    and self.is_valid_part(C) \
                                    and self.is_valid_part(D):
                                ans.append('.'.join([A, B, C, D]))
        return ans

    def is_valid_part(self, s: str):
        return s != '' and 0 <= int(s) <= 255 and (s[0] != '0' or s == '0')  # 第一位不是 0 或者本身就是 0:


class _Test(unittest.TestCase):
    def test(self):
        _input = '25525511135'
        _output = Solution().restoreIpAddresses(_input)
        _expect = ["255.255.11.135", "255.255.111.35"]
        self.assertListEqual(_expect, _output)
