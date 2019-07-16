from leetcode import TreeNode


class AvlTree(TreeNode):
    """
    太难了

    这是数据结构书上实现，个人感觉太绕太难理解了
    """

    def __init__(self, x):
        super().__init__(x)
        self.bf = 0

    @classmethod
    def from_array(cls, array, index=0):
        """
        >>> AvlTree.from_array([30,40,50]).to_num_with_comma()#右右，左旋
        '40,30,50'
        >>> AvlTree.from_array([50,40,30]).to_num_with_comma()#左左，右旋
        '40,30,50'
        >>> AvlTree.from_array([50,30,40]).to_num_with_comma()#左右，左右旋
        '40,30,50'
        >>> AvlTree.from_array([30,50,40]).to_num_with_comma()#右左，右左旋
        '40,30,50'
        >>> AvlTree.from_array([50,30,70,20,40]).to_num_with_comma()#左右情况初始
        '50,30,70,20,40'
        >>> AvlTree.from_array([50,30,70,20,40,35]).to_num_with_comma()#左右左，左右旋
        '40,30,50,20,35,70'
        >>> AvlTree.from_array([50,30,70,20,40,45]).to_num_with_comma()#左右右，左右旋
        '40,30,50,20,45,70'
        >>> AvlTree.from_array([50,30,70,60,80]).to_num_with_comma()#右左情况初始
        '50,30,70,60,80'
        >>> AvlTree.from_array([50,30,70,60,80,65]).to_num_with_comma()#右左右，右左旋
        '60,50,70,30,65,80'
        >>> AvlTree.from_array([50,30,70,60,80,55]).to_num_with_comma()#右左左，右左旋
        '60,50,70,30,55,80'
        """
        if not array:
            return AvlTree(0)
        root = AvlTree(array[0])
        for i in range(1, len(array)):
            root, _ = cls.insert(root, array[i])
        return root

    @staticmethod
    def insert(tree, x):
        if not tree:
            # 插入结点，长高
            tree = AvlTree(x)
            return tree, True
        if x == tree.val:
            # 不允许有相等值
            return None, False
        if x < tree.val:
            # 插入左边
            tree.left, tall = AvlTree.insert(tree.left, x)
            if not tree.left:
                # 插入失败
                return tree, False
            if tall:
                # 长高
                if tree.bf == 1:
                    # 原本就左边高，需要左平衡
                    return AvlTree.left_balance(tree), False
                elif tree.bf == 0:
                    # 左②，原本等高，现在左边高
                    tree.bf = 1
                    return tree, True
                else:
                    # 左③，原本右边高，现在等高
                    tree.bf = 0
                    return tree, False
            else:
                # 左①，未长高
                return tree, False
        else:
            # 插入右边
            tree.right, tall = AvlTree.insert(tree.right, x)
            if not tree.right:
                # 插入失败
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
            # 左④，新结点插在左孩子的左子树上，左左，执行右旋，右旋后平衡因子者为 0
            tree.bf = lc.bf = 0
            return AvlTree.right_rotate(tree)
        elif lc.bf == -1:
            # 新结点插在左孩子的右子树上，左右，执行双旋 
            rd = lc.right
            if rd.bf == 1:
                # 左⑥，根1，左子树-1，右子树 1
                # 这和情况下，先左旋，再右旋，根旋转到右侧，平衡因子变为 -1
                tree.bf = -1
                lc.bf = 0
            elif rd.bf == 0:
                # 左⑤，右子树平衡因子为 0，形成标准的左右形式
                # 先左旋，再右旋，最后 tree 和 left 平衡因子都为0
                tree.bf = lc.bf = 0
            else:
                # 左⑦，根1，左子树-1，右子树-1
                tree.bf = 0
                lc.bf = 1
            rd.bf = 0
            tree.left = AvlTree.left_rotate(tree.left)
            return AvlTree.right_rotate(tree)

    @staticmethod
    def right_balance(tree):
        rc = tree.right
        if rc.bf == -1:
            # 右右，执行左旋
            tree.bf = rc.bf = 0
            return AvlTree.left_rotate(tree)
        elif rc.bf == 1:
            # 右孩子的左子树上
            ld = rc.left
            if ld.bf == 0:
                # 标准的右左，先右旋，再左旋
                tree.bf = rc.bf = 0
            elif ld.bf == -1:
                # 右子树的左孩子，添加了右叶子
                # 在右旋时，该右叶子成为右子树的左叶子，使得右子树平衡因子变为 0
                # 再左旋时，根下移成为 ld 的左孩子，平衡因子变为1
                tree.bf = 1
                rc.bf = 0
            else:
                # 右子树的左孩子，添加了左叶子
                # 在右旋时，右子树下移，成为 ld 的右孩子，平衡因子变为-1
                # 该左叶子在右旋、左旋后，成为根的右叶子，使根的平衡因子变为 0
                tree.bf = 0
                rc.bf = -1
            ld.bf = 0
            tree.right = AvlTree.right_rotate(tree.right)
            return AvlTree.left_rotate(tree)

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


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
