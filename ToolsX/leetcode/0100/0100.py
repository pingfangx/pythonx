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
        if p and not q:  # 可以优化，根据前面的判断，不可能能两者都为空
            return False
        if q and not p:
            return False
        if p.val != q.val:
            return False
        if not self.isSameTree(p.left, q.left):
            return False
        if not self.isSameTree(p.right, q.right):
            return False
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
