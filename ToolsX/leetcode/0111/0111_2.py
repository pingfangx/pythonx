from leetcode import TreeNode


class Solution:
    def minDepth(self, root: TreeNode) -> int:
        """

        如果求最大深度，我们需要每个结点都遍历
        而最小深度的话，如果超过，应该不需要了

        1
        广度优先

        2
        一开始的思路是对的，优化
        """
        if not root:
            return 0
        left = self.minDepth(root.left)
        right = self.minDepth(root.right)
        return 1 + (left + right if not left or not right else min(left, right))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
