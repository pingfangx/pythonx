from typing import List

from twisted.trial import unittest


class Solution:
    """20190816"""

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        简单理一下思路

        遇到一个字符串，就列出所有的可能，如果后续属于可能，则加进指定数组中，但是这样的话，列出所有可能组合可能会是冗余的
        复杂度来源于列出所有可能

        遇到一个字符串，对其进行排序，然后匹配
        复杂度来源于排序

        1 Pythonic
        """
        ans = {}
        for i in strs:
            key = tuple(sorted(i))
            ans[key] = ans.get(key, []) + [i]
        return list(ans.values())


class _Test(unittest.TestCase):
    def test(self):
        _input = ["eat", "tea", "tan", "ate", "nat", "bat"]
        _output = Solution().groupAnagrams(_input)
        _expect = [
            ["ate", "eat", "tea"],
            ["nat", "tan"],
            ["bat"]
        ]
        self.assertListEqual(_expect, _output)
