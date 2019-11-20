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
        >>> Solution().isValidBST(TreeNode.from_array([3,None,30,10,None,None,15,None,45]))
        False
        >>> Solution().isValidBST(TreeNode.from_array([5,1,4,None,None,3,6]))
        False
        """
        if not root:
            return True
        stack = [(root, float('-inf'), float('inf'))]
        while stack:
            node, lower, upper = stack.pop()
            if not node:
                continue
            val = node.val
            if val <= lower or val >= upper:
                return False
            stack.append((node.right, val, upper))
            stack.append((node.left, lower, val))  # 后添加 left 深度优先
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
