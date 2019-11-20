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
        >>> Solution().inorderTraversal(TreeNode.from_args(1,None,2,3))
        [1, 3, 2]
        """
        ans = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node:
                if node.left or node.right:
                    if node.right:
                        stack.append(node.right)  # right 最先添加最后读取
                        node.right = None
                    if node.left:
                        stack.append(node)
                        stack.append(node.left)  # 添加 node 和 left，让 left 先于 node
                        node.left = None
                    else:  # 不需要再添加 node 直接取值
                        ans.append(node.val)
                else:
                    ans.append(node.val)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
