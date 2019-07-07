from leetcode import TreeNode


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        """
        减去 root，然后继续判断 child

        1
        仅仅了解皮毛，不会合理使用
        """
        if not root:
            return False
        dif = sum - root.val  # 本来想着多一个变量，可以省去后面的计算，结果内存占用增加了
        if dif == 0 and not root.left and not root.right:
            # 如果相等且没有子结点，则返回，如果有子结点不需要返回 false，后续可能再累加回 0
            return True
        return self.hasPathSum(root.left, dif) or self.hasPathSum(root.right, dif)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
