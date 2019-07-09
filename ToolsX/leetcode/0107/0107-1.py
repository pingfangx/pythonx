from typing import List

from leetcode import TreeNode


class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        """
        BFS
        插入最前

        1
        递归，万恶的递归
        """
        data = []
        self.level_order_bottom(data, 1, root)
        return data

    def level_order_bottom(self, data, depth, tree):
        if tree:
            if len(data) < depth:
                data.insert(0, [])
            data[-depth].append(tree.val)
            self.level_order_bottom(data, depth + 1, tree.left)
            self.level_order_bottom(data, depth + 1, tree.right)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
