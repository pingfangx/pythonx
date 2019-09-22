from typing import List

from leetcode import TreeNode


class Solution:
    """20190922"""

    def inorderTraversal(self, root: TreeNode) -> List[int]:
        """
        中序，题目要求不用递归，使用迭代
        先用递归实现

        1
        如何使用迭代，一般应该是配合栈

        2
        1 中类似广度，答案提供了先深度到底
        >>> Solution().inorderTraversal(TreeNode.from_args(1,None,2,3))
        [1, 3, 2]
        """
        res = []
        stack = []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
