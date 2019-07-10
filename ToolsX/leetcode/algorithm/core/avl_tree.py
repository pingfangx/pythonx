from leetcode import TreeNode


class AvlTree(TreeNode):
    """太难了，我不会啊"""

    def __init__(self, x):
        super().__init__(x)
        self.bf = 0

    @classmethod
    def from_array(cls, array, index=0):
        if not array:
            return AvlTree(0)
        root = AvlTree(array[0])
        for i in range(1, len(array)):
            root = cls.insert(root, array[i])
        return root

    @staticmethod
    def insert(tree, x):
        if not tree:
            # 插入结点，长高
            tree = AvlTree(x)
            return tree, True
        if x == tree.val:
            return tree, False
        if x < tree.val:
            # 插入左边
            tree.left, tall = AvlTree.insert(tree.left, x)
            if not tree.left:
                return tree, False
            if tall:
                # 长高
                if tree.bf == 1:
                    # 原本左边高，需要左平衡
                    return AvlTree.left_balance(tree), False
                elif tree.bf == 0:
                    # 原本等高，现在左边高
                    tree.bf = 1
                    return tree, True
                else:
                    # 原本右边高，现在等高
                    tree.bf = 0
                    return tree, False
            else:
                return tree, False
        else:
            # 插入右边
            tree.right, tall = AvlTree.insert(tree.right, x)
            if not tree.right:
                return tree, False
            if tall:
                # 长高
                if tree.bf == 1:
                    # 原本左边高，现在等高
                    tree.bf = 0
                    return tree, False
                elif tree.bf == 0:
                    # 原本等高，现在右边高
                    tree.bf = -1
                    return tree, True
                else:
                    # 原本右边高，需要右平衡
                    return AvlTree.right_balance(tree), False
            else:
                return tree, False

    @staticmethod
    def left_balance(tree):
        lc = tree.left
        if lc.bf == 1:
            # 左边高，左左
            tree.bf = lc.bf = 0
            return AvlTree.left_rotate(tree)
        elif lc.bf == -1:
            # 右边高，左右
            rd = lc.right
            if rd.bf == 1:
                tree.bf = -1
                lc.bf = 0
            elif rd.bf == 0:
                tree.bf = lc.bf = 0
            else:
                tree.bf = 0
                lc.bf = 1
            rd.bf = 0
            tree.left = AvlTree.left_rotate(tree.left)
            return AvlTree.right_rotate(tree)

    @staticmethod
    def right_balance(tree):
        pass

    @staticmethod
    def left_rotate(tree):
        rc = tree.right
        tree.right = rc.left
        rc.left = tree
        return rc

    @staticmethod
    def right_rotate(tree):
        lc = tree.left
        tree.left = lc.right
        lc.right = tree
        return lc
