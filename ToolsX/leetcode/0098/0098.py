from leetcode import TreeNode


class Solution:
    """20190926"""

    def isValidBST(self, root: TreeNode) -> bool:
        """
        要注意比较左边最大的和右边最小的
        答案中还有很多解法，可以学习一下
        >>> Solution().isValidBST(TreeNode.from_array([3,None,30,10,None,None,15,None,45]))
        False
        >>> Solution().isValidBST(TreeNode.from_array([5,1,4,None,None,3,6]))
        False
        """
        if not root:
            return True
        if root.left:
            if root.left.val >= root.val:
                return False
            if self.right_most(root.left).val >= root.val:
                return False
        if root.right:
            if root.right.val <= root.val:
                return False
            if self.left_most(root.right).val <= root.val:
                return False
        return self.isValidBST(root.left) and self.isValidBST(root.right)

    def right_most(self, root: TreeNode) -> TreeNode:
        while root.right:
            root = root.right
        return root

    def left_most(self, root: TreeNode) -> TreeNode:
        while root.left:
            root = root.left
        return root


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
