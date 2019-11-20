from leetcode import TreeNode


class Solution:
    """20190927"""

    def recoverTree(self, root: TreeNode) -> None:
        """
        前 100 中的最后一题，后续不会再按顺序刷了
        可能会解决自己感兴趣的题目，或者是练习某些 tag
        从7月1日第一题开始，马上就十一了，连续做了 3 个月的题，保证每天都有一题。
        虽然感觉有些难题自己还是思路不太好，但也聊胜于无，加油。

        回到这一题 0098 中的一些 trick 应该用不了，还是要老老实实判断当前结点下是否合法，不合法则找出应该和哪一个交换

        折腾了一会儿，还是做不出来
        >>> root=TreeNode.from_leetcode_array_str('[1,3,null,null,2]')
        >>> Solution().recoverTree(root)
        >>> root.to_leetcode_array_str()
        '[3,1,null,null,2]'
        """
        print(root.to_tree_graph())
        bad = self.find_bad(root, float('-inf'), float('inf'))
        if bad:
            node = bad[0]
            replace = self.replace(root, *bad[1:])
            node.val, replace.val = replace.val, node.val

    def find_bad(self, root: TreeNode, lower, upper):
        if not root:
            return None
        # 优先返回子结点
        left = self.find_bad(root.left, lower, upper)
        if left:
            return left
        right = self.find_bad(root.right, lower, upper)
        if right:
            return right

        val = root.val
        if val <= lower or val >= upper:
            return root, val, lower, upper
        res = self.find_bad(root.left, lower, val)
        if res:
            return res
        res = self.find_bad(root.right, val, upper)
        if res:
            return res
        return None

    def replace(self, root, val, lower, upper):
        if not root:
            return None
        if self.valid(root, val, lower, upper):
            return root
        res = self.replace(root.left, val, lower, upper)
        if res:
            return res
        return self.replace(root.right, val, lower, upper)

    def valid(self, root, val, lower, upper):
        if not root:
            return False
        if root.val < lower or root.val > upper:  # 可能就是要替换的结点，可以 =
            return False
        if root.left and root.left.val > val:
            return False
        if root.right and root.right.val < val:
            return False
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
