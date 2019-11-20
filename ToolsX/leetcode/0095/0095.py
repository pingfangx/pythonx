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
        """
        if not n:
            return []
        nums = list(range(1, n + 1))
        ans = {}
        self.helper(ans, None, nums)
        return list(ans.values())

    def helper(self, ans: dict, pre: TreeNode, nums: List[int]):
        if not nums:
            tree = self.copy(pre)
            node_str = self.node_str(tree)
            if node_str not in ans:
                ans[node_str] = tree
        else:
            for i, num in enumerate(nums):
                nums.remove(num)
                if pre is None:
                    self.helper(ans, TreeNode(num), nums)
                else:
                    if self.insert(pre, num):  # 成功插入才继续
                        self.helper(ans, pre, nums)
                        self.delete(pre, num)
                nums.insert(i, num)

    def node_str(self, root: TreeNode):
        nodes = []
        stack = [root]
        while stack:
            node = stack.pop(0)
            if node:
                nodes.append(str(node.val))
                if node.left or node.right:
                    stack.append(node.left)
                    stack.append(node.right)
            else:
                nodes.append('null')
        return ','.join(nodes)

    def copy(self, source: TreeNode) -> TreeNode:
        if not source:
            return source
        res = TreeNode(source.val)
        res.left = self.copy(source.left)
        res.right = self.copy(source.right)
        return res

    def insert(self, root: TreeNode, num: int) -> TreeNode:
        if not root:
            return TreeNode(num)
        if num < root.val:
            root.left = self.insert(root.left, num)
        else:
            root.right = self.insert(root.right, num)
        return root

    def delete(self, root: TreeNode, num: int) -> TreeNode:
        if not root:
            return None
        if num == root.val:
            return None
        elif num < root.val:
            root.left = self.delete(root.left, num)
        else:
            root.right = self.delete(root.right, num)
        return root


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
