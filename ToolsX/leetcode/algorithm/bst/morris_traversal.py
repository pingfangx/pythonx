from twisted.trial import unittest

from leetcode import TreeNode


def morris_inorder_traversal(root: TreeNode):
    cur = root
    while cur:
        if not cur.left:  # 没有左，指向右
            print(cur.val)
            cur = cur.right
        else:  # 有左，查找最右边，连接 cur
            pre = cur.left
            while pre.right and pre.right != cur:
                pre = pre.right
            if not pre.right:
                pre.right = cur
                cur = cur.left
            else:  # pre.right==cur 还原为空
                pre.right = None
                print(cur.val)
                cur = cur.right


class _Test(unittest.TestCase):
    def test(self):
        tree = TreeNode.from_iter(range(1, 10))
        print(tree)
        print()
        morris_inorder_traversal(tree)
