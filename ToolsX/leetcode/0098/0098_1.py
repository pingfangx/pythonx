from leetcode import TreeNode


class Solution:
    """20190926"""

    def isValidBST(self, root: TreeNode) -> bool:
        """
        要注意比较左边最大的和右边最小的
        答案中还有很多解法，可以学习一下

        https://leetcode.com/problems/validate-binary-search-tree/solution/
        >>> Solution().isValidBST(TreeNode.from_array([3,None,30,10,None,None,15,None,45]))
        False
        >>> Solution().isValidBST(TreeNode.from_array([5,1,4,None,None,3,6]))
        False
        """

        def helper(node, lower=float('-inf'), upper=float('inf')):
            if not node:
                return True
            val = node.val
            if val <= lower or val >= upper:
                return False
            if not helper(node.left, lower, val):  # 左边的比 val 小
                return False
            if not helper(node.right, val, upper):  # 右边的比 val 大
                return False
            return True

        return helper(root)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
