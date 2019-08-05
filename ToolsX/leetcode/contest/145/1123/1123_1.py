from leetcode import TreeNode


class Solution:
    def lcaDeepestLeaves(self, root: TreeNode) -> TreeNode:
        """
        不正确，题目不是完全二叉树
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(12345)).to_num()
        245
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(123)).to_num()
        123
        >>> Solution().lcaDeepestLeaves(TreeNode.from_num(1234)).to_num()
        4
        >>> Solution().lcaDeepestLeaves(TreeNode.from_array([1,None,2,None,3,None,4,None,5])).to_num()
        5
        """

        def depth_find(root, find):  # 查找在哪一层
            if not root:
                return 0
            if root == find:
                return 1
            else:
                left = depth_find(root.left, find)
                if left:
                    return 1 + left
                right = depth_find(root.right, find)
                if right:
                    return 1 + right

        def depth(root):  # 深度
            return 0 if not root else (1 + max(depth(root.left), depth(root.right)))

        if not root or not root.val:
            return None
        if not root.left and not root.right:  # 没有根结点，返回当前
            return root
        left = self.lcaDeepestLeaves(root.left)
        right = self.lcaDeepestLeaves(root.right)
        if not left:
            return right
        if not right:
            return left

        # 找到左右，判断深度
        depth_left = depth_find(root, left) + depth(left)
        depth_right = depth_find(root, right) + depth(right)
        if depth_left > depth_right:  # 返回较深者
            return left
        elif depth_right > depth_left:
            return right
        else:  # 深度相等，返回 parent
            return root


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
