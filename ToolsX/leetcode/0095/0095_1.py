from typing import List

from twisted.trial import unittest

from leetcode import TreeNode


class Solution:
    """20190923"""

    def generateTrees(self, n: int) -> List[TreeNode]:
        """
        折腾了一番，如何处理重复呢
        取为字符串判断重复，又笨又慢
        看了计论，有点心累

        1

        """
        if not n:
            return []
        return self.generate_trees(1, n)

    def generate_trees(self, start: int, end: int):
        res = []
        if start > end:
            res.append(None)
        for i in range(start, end + 1):
            left_list = self.generate_trees(start, i - 1)
            right_list = self.generate_trees(i + 1, end)
            for left in left_list:
                for right in right_list:
                    root = TreeNode(i)
                    root.left = left
                    root.right = right
                    res.append(root)
        return res


class _Test(unittest.TestCase):
    def test(self):
        _input = 3
        _output = Solution().generateTrees(_input)
        _expect = [
            [1, None, 3, 2],
            [3, 2, None, 1],
            [3, 1, None, None, 2],
            [2, 1, 3],
            [1, None, 2, None, 3]
        ]
        self.assertListEqual(_expect, _output)
