import queue
import random

from leetcode.core import tree_utils


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __str__(self):
        return self.to_tree_graph()

    def __repr__(self):
        return self.__str__()

    def trim(self):
        """
        使用队列，按行添加
        """
        s = ''
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            node = q.get()
            s += str(node.val)
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
        return s

    def to_array(self):
        array = []
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            node = q.get()
            if node:
                array.append(node.val)
                if node.left or node.right:  # 有一个为空就添加
                    q.put(node.left)
                    q.put(node.right)
            else:
                array.append(None)
        return array

    def to_num(self):
        """
        >>> TreeNode.from_num(123456).to_num()
        123456
        """
        return int(self.trim())

    def to_num_with_comma(self):
        """数字和逗号"""
        s = ''
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            node = q.get()
            s += str(node.val) + ','
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
        if s:
            s = s[:-1]
        return s

    def to_tree_graph(self):
        """
        转为树图
        >>> TreeNode.create(20).to_tree_graph()
        """
        return tree_utils.to_tree_graph(self)

    @classmethod
    def from_array(cls, array, index=0):
        """
        >>> TreeNode.from_array([1,None,2,None,3,None,4,None,5]).to_num()
        12345
        >>> TreeNode.from_array([1,2,None,3,None,4,None,5]).to_num()
        """
        n = len(array)
        if n == 0:
            return TreeNode(0)
        elif n == 1:
            if array[index] is None:
                return None
            else:
                return TreeNode(array[index])
        else:
            node = TreeNode(array[index])
            # 0 -> 1,1->3
            left_index = (index + 1) * 2 - 1
            right_index = (index + 1) * 2
            if left_index < n and right_index < n and (not array[left_index] or not array[right_index]):
                # 根据层先法遍历，如果一个结点为空，那么后续数组中的值就不再属于这个节点
                if not array[left_index] and not array[right_index]:
                    node.left = None
                    node.right = None
                elif not array[left_index]:
                    node.right = cls.from_array(array[right_index:])
                elif not array[right_index]:
                    t = [array[left_index]] + array[right_index + 1:]
                    node.left = cls.from_array(t)
            else:
                if left_index < len(array):
                    node.left = cls.from_array(array, left_index)
                if right_index < len(array):
                    node.right = cls.from_array(array, right_index)
        return node

    @classmethod
    def from_iter(cls, iterable):
        # else 处理为 None 的情况
        return cls.from_array([int(i) if i else i for i in iterable])

    @classmethod
    def from_args(cls, *args):
        return cls.from_iter(list(args))

    @classmethod
    def from_str(cls, values: str):
        return cls.from_iter(values)

    @classmethod
    def from_num(cls, num: int):
        return cls.from_str(str(num))

    @classmethod
    def create(cls, length=5, start=1, rand_max=10, rand=False):
        array = [i if not rand else random.randint(start, rand_max) for i in range(start, start + length)]
        return cls.from_array(array)

    @classmethod
    def random(cls, length=5, **kwargs):
        return cls.create(length, rand=True, **kwargs)

    @classmethod
    def from_leetcode_array_str(cls, string: str):
        return cls.from_array([None if i == 'null' else int(i) for i in string.strip('[]').split(',')])

    def to_leetcode_array_str(self) -> str:
        return str(self.to_array()).replace(' ', '').replace('None', 'null')


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=TreeNode)
