from typing import List

from leetcode import TreeNode


class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        """
        BFS
        插入最前

        1
        递归，万恶的递归

        2 在使用队列时，不需要一个新的 tmp 只需要记录大小就可以了
        """
        if not root:
            return []
        data = []
        q = [root]
        while q:
            line = []
            for i in range(len(q)):
                t = q.pop(0)
                line.append(t.val)
                if t.left:
                    q.append(t.left)
                if t.right:
                    q.append(t.right)
            data.insert(0, line)
        return data


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
