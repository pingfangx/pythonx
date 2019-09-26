from leetcode import TreeNode


class Solution:
    """20190926"""

    def isValidBST(self, root: TreeNode) -> bool:
        """
        要注意比较左边最大的和右边最小的
        答案中还有很多解法，可以学习一下

        https://leetcode.com/problems/validate-binary-search-tree/solution/

        1 中是递归

        2 改为迭代，迭代一般要使用栈，还是使用 lower,upper

        3
        中序，先迭代到最左边
        while 要判断栈和 root
        >>> Solution().isValidBST(TreeNode.from_array([3,None,30,10,None,None,15,None,45]))
        False
        >>> Solution().isValidBST(TreeNode.from_array([5,1,4,None,None,3,6]))
        False
        """
        if not root:
            return True
        pre_val = float('-inf')
        stack = []
        while stack or root:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            if root.val <= pre_val:
                return False
            pre_val = root.val
            root = root.right
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
