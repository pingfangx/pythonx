from leetcode import TreeNode


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        """
        用队列试一下
        """
        if not root:
            return 0
        depth = 0
        q = [root]
        while q:
            depth += 1
            # 将本层清空
            tq = []
            while q:
                t = q.pop()
                if t.left:
                    tq.append(t.left)
                if t.right:
                    tq.append(t.right)
            q.extend(tq)
        return depth


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
