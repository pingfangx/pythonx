from leetcode import TreeNode


class AvlTree(TreeNode):
    """
    这一种实现来自
    https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
    感觉比较好理解
    """

    def __init__(self, x):
        super().__init__(x)
        self.height = 1

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
            root = root.insert(root, array[i])
        return root

    def insert(self, root, x):
        # 1 执行插入
        if not root:
            return AvlTree(x)
        elif x < root.val:  # 插入可能会导致其结点变化，所以需要重新赋值
            root.left = self.insert(root.left, x)
        else:
            root.right = self.insert(root.right, x)

        # 2 更新高度
        root.height = self.calculate_height(root)

        # 3 获取平衡因子
        balance = self.get_balance(root)

        # 4 如果不平衡，判断并旋转
        if balance > 1:  # 左边高
            if x < root.left.val:  # 左左
                return self.right_rotate(root)
            elif x > root.left.val:  # 左右
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        elif balance < -1:  # 右边高
            if x > root.right.val:  # 右右
                return self.left_rotate(root)
            elif x < root.right.val:  # 右左
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        return root  # 无旋转返回 root

    def delete(self, root, x):
        if not root:
            return root
        if x < root.val:
            root.left = self.delete(root.left, x)
        elif x > root.val:
            root.right = self.delete(root.right, x)
        else:  # 找到结点，进行删除
            if not root.left:  # 没有左结点
                t, root = root.right, None
                return t
            elif not root.right:  # 没有右结点
                t, root = root.left, None
                return t
            else:  # 都有
                t = self.get_min_value_node(root.right)
                root.val = t.val
                root.right = self.delete(root.right, t.val)
        # ①如果只有一个结点，删除后为空
        if not root:
            return root

        # 2 更新高度
        root.height = self.calculate_height(root)

        # 3 获取平衡因子
        balance = self.get_balance(root)

        # 4 如果不平衡，判断并旋转
        if balance > 1:  # 左边高
            if self.get_balance(root.left) >= 0:  # 左左
                return self.right_rotate(root)
            elif self.get_balance(root.left) < 0:  # 左右
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        elif balance < -1:  # 右边高
            if self.get_balance(root.right) <= 0:  # 右右
                return self.left_rotate(root)
            elif self.get_balance(root.right) > 0:  # 右左
                root.right = self.left_rotate(root.right)
                return self.right_rotate(root)

        return root  # 无旋转返回 root

    def get_height(self, root):
        """获取高度

        因为创建时会初始化高度，增加高度只会通过插入结点，在插入时高度会再计算
        """
        return 0 if not root else root.height

    def calculate_height(self, root):
        return 0 if not root else (1 + max(self.get_height(root.left), self.get_height(root.right)))

    def get_balance(self, root):
        """获取平衡因子"""
        return 0 if not root else (self.get_height(root.left) - self.get_height(root.right))

    def get_min_value_node(self, root):
        """获取最小值的结点"""
        if not root or not root.left:
            return root
        return self.get_min_value_node(root.left)

    def left_rotate(self, root):
        rc = root.right
        root.right = rc.left
        rc.left = root

        # 重新计算高度
        self.calculate_height(root)
        self.calculate_height(rc)
        return rc

    def right_rotate(self, root):
        lc = root.left
        root.left = lc.right
        lc.right = root

        # 重新计算高度
        self.calculate_height(root)
        self.calculate_height(lc)
        return lc


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
