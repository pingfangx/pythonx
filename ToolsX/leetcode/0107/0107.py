from typing import List

from leetcode import TreeNode


class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        """
        BFS
        插入最前
        """
        if not root:
            return []
        r = []
        q = [root]
        while q:
            tmp = []
            values = []
            while q:
                node = q.pop(0)
                values.append(node.val)
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            # 添加完一层
            r.insert(0, values)
            q = tmp
        return r


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
