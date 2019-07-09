from leetcode import TreeNode


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        """
        用队列试一下

        1
        讨论中的方法，树就应该多用递归
        """
        return 0 if root is None else 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
