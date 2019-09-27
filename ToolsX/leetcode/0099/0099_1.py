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

        1
        https://leetcode.com/problems/recover-binary-search-tree/discuss/32535/No-Fancy-Algorithm-just-Simple-and-Powerful-In-Order-Traversal
        思路就是在前序遍历中，前面的元素应该小于后面的元素，如果不小于，则认为是错误的位置
        >>> root=TreeNode.from_leetcode_array_str('[1,3,null,null,2]')
        >>> Solution().recoverTree(root)
        >>> root.to_leetcode_array_str()
        '[3,1,null,null,2]'
        """
        nodes = [None, None, None]  # pre,first,second
        self.traverse(root, nodes)
        if nodes[1] and nodes[2]:
            nodes[1].val, nodes[2].val = nodes[2].val, nodes[1].val

    def traverse(self, root, nodes):
        if not root:
            return
        self.traverse(root.left, nodes)
        pre = nodes[0]
        # If first element has not been found, assign it to prevElement
        if not nodes[1] and (pre is None or pre.val >= root.val):
            nodes[1] = pre  # 当第一次遇到不正确的顺序时，nodes[0] 和 nodes[1] 同时赋值，后续只更新 nodes[1]
        if nodes[1] and pre.val >= root.val:  # If first element is found, assign the second element to the root
            nodes[2] = root
        nodes[0] = root
        self.traverse(root.right, nodes)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
