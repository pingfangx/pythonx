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

        1
        不重复计算
        在计算高度的同时，判断是否是平衡二叉树，如果不是，返回 -1 作为标识
        """
        return self.depth(root) != -1

    def depth(self, root: TreeNode) -> int:
        if not root:
            return 0
        left_high = self.depth(root.left)
        right_high = self.depth(root.right)
        if left_high == -1 or right_high == -1 or abs(left_high - right_high) > 1:
            return -1
        return 1 + max(left_high, right_high)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
