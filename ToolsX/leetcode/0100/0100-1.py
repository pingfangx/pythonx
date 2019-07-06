from leetcode import TreeNode


class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        """
        >>> p=TreeNode.from_num(12345)
        >>> q=TreeNode.from_args(1,2,3,4,5)
        >>> Solution().isSameTree(p,q)
        True
        """
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
