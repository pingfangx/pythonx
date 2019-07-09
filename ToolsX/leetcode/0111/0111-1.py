from leetcode import TreeNode


class Solution:
    def minDepth(self, root: TreeNode) -> int:
        """

        如果求最大深度，我们需要每个结点都遍历
        而最小深度的话，如果超过，应该不需要了

        1
        广度优先
        """
        if not root:
            return 0
        q = [root]
        depth = 0
        while q:
            depth += 1
            for i in range(len(q)):
                t = q.pop(0)
                if not t.left and not t.right:
                    # 没有子结点，返回
                    return depth
                if t.left:
                    q.append(t.left)
                if t.right:
                    q.append(t.right)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
