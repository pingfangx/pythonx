from leetcode import TreeNode


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        """
        平衡二叉树

        按定义来，左右两边高度差小于 1 且左右两边是平衡二叉树

        时间复杂度
        求 depth 每个结点都要判断 n
        而对每个结点都要判断 isBalanced
        O(n^2)

        可以看到度深度计算其实是有重复的
        """
        if not root:
            return True
        if abs(self.depth(root.left) - self.depth(root.right)) > 1:
            return False
        return self.isBalanced(root.left) and self.isBalanced(root.right)

    def depth(self, root: TreeNode) -> int:
        return 0 if not root else 1 + max(self.depth(root.left), self.depth(root.right))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
