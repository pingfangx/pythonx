from leetcode import TreeNode


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        """
        根据 0100 中判断相等的，只需要判断 p.left==q.right and p.right==q.left
        但是时间和空间都不少

        1
        答案中的迭代
        一开始想用队列的，但是发现不好比较，其实就是每次取出两个就好了
        >>> Solution().isSymmetric(TreeNode.from_array([1,2,2,None,3,None,3]))
        """
        if not root:
            return True
        q = [root.left, root.right]
        while q:
            t1 = q.pop(0)
            t2 = q.pop(0)
            if not t1 and not t2:
                # 为空也就不需要添加子结点
                continue
            if not t1 or not t2:
                return False
            if t1.val != t2.val:
                # 值
                return False
            q.append(t1.left)
            q.append(t2.right)
            q.append(t1.right)
            q.append(t2.left)
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
