from leetcode import TreeNode


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        """
        减去 root，然后继续判断 child
        """
        if not root:
            # return sum == 0
            return False
        dif = sum - root.val
        if dif == 0:
            if not root.left and not root.right:
                # 可能后续还有
                return True
        if root.left and self.hasPathSum(root.left, dif):
            return True
        if root.right and self.hasPathSum(root.right, dif):
            return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
