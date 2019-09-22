from typing import List

from leetcode import TreeNode


class Solution:
    """20190922"""

    def inorderTraversal(self, root: TreeNode) -> List[int]:
        """
        中序，题目要求不用递归，使用迭代
        先用递归实现
        >>> Solution().inorderTraversal(TreeNode.from_args(1,None,2,3))
        [1, 3, 2]
        """
        ans = []
        self.inorder(ans, root)
        return ans

    def inorder(self, ans: List[int], root: TreeNode):
        if root:
            if root.left:
                self.inorder(ans, root.left)
            ans.append(root.val)
            if root.right:
                self.inorder(ans, root.right)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
