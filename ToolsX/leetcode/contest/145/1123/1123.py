from leetcode import TreeNode


class Solution:
    def lcaDeepestLeaves(self, root: TreeNode) -> TreeNode:
        """
        不正确，题目不是完全二叉树
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(123)).to_num()
        123
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(1234)).to_num()
        4
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(12345)).to_num()
        245
        """

        def depth(root):  # 深度
            return 0 if not root else (1 + max(depth(root.left), depth(root.right)))

        def count(root):  # 数量
            return 0 if not root else (1 + count(root.left) + count(root.right))

        def get_at_depth(root, n):
            if not root:
                return None
            if n == 1:
                return root
            else:
                left = get_at_depth(root.left, n - 1)
                if left:
                    return left
                right = get_at_depth(root.right, n - 1)
                if right:
                    return right

        d = depth(root)
        c = count(root)
        leaves = c - (2 ** (d - 1) - 1)
        # 需要降低 log2(leaves) 层
        n = -1
        while leaves:
            leaves >>= 1
            n += 1
        return get_at_depth(root, d - n)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
