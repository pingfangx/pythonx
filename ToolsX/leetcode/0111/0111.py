from leetcode import TreeNode


class Solution:
    def minDepth(self, root: TreeNode) -> int:
        """

        如果求最大深度，我们需要每个结点都遍历
        而最小深度的话，如果超过，应该不需要了
        """
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        if root.left and root.right:
            return 1 + min(self.minDepth(root.left), self.minDepth(root.right))
        if root.left:
            return 1 + self.minDepth(root.left)
        if root.right:
            return 1 + self.minDepth(root.right)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
