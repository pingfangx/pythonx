import math
import queue
import random


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
        使用对列，按行添加
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
            array.append(node.val)
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
        return array

    def to_num(self):
        """
        >>> TreeNode.from_num(123456).to_num()
        123456
        """
        return int(self.trim())

    def to_tree_graph(self):
        """
        >>> TreeNode.create(20).to_tree_graph()
        """
        array = self.to_array()
        depth = int(math.log2(len(array))) + 1
        lines = []
        for i in range(depth):
            line = []
            lines.append(line)
            for j in range(2 ** i - 1, 2 ** (i + 1) - 1):
                if j < len(array):
                    line.append(array[j])
                else:
                    line.append(' ')
        max_length = 2 ** depth
        for i in range(len(lines)):
            while len(lines[i]) < max_length:
                lines[i] = ''.join([' ' + str(i) for i in lines[i]])
        return '\n'.join([''.join(line) for line in lines])

    @classmethod
    def from_array(cls, array, index=0):
        if len(array) == 0:
            return TreeNode(0)
        elif len(array) == 1:
            return TreeNode(array[index])
        else:
            node = TreeNode(array[index])
            # 0 -> 1,1->3
            left_index = (index + 1) * 2 - 1
            right_index = (index + 1) * 2
            if left_index < len(array):
                node.left = cls.from_array(array, left_index)
            if right_index < len(array):
                node.right = cls.from_array(array, right_index)
        return node

    @classmethod
    def from_iter(cls, iterable):
        return cls.from_array([int(i) for i in iterable])

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


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=TreeNode)
