from leetcode import TreeNode


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        """
        根据 0100 中判断相等的，只需要判断 p.left==q.right and p.right==q.left
        但是时间和空间都不少
        """
        return not root or self.isSameTree(root.left, root.right)

    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.right) and self.isSameTree(p.right, q.left)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
