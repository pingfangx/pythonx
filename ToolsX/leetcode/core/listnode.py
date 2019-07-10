import random


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x: int):
        self.val = x
        self.next = None

    def __str__(self):
        if self.has_cycle():
            return 'cycle'
        return f'{self.val}' + ('' if not self.next else f' -> {self.next}')

    def __repr__(self):
        return self.__str__()

    def trim(self):
        # 也可以正则
        return self.__str__().replace(' ', '').replace('-', '').replace('>', '')

    def to_number(self):
        return int(self.trim())

    def to_array(self):
        """转为数组"""
        if self.has_cycle():
            return 'cycle'
        t = []
        p = self
        while p:
            t.append(p.val)
            p = p.next
        return t

    def has_cycle(self) -> bool:
        slow = fast = self
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if id(slow) == id(fast):
                return True
        return False

    def append_tail(self, node):
        if isinstance(node, ListNode):
            self.get_tail().next = node
            return self
        else:
            return self.append_tail(ListNode(node))

    def get_tail(self):
        tail = self
        while tail.next:
            tail = tail.next
        return tail

    @classmethod
    def create(cls, length=5, start=1, end=10, rand=False):
        if length == 0:
            return None
        node = ListNode(start if not rand else random.randrange(start, end))
        if length == 1:
            return node
        current = node
        for i in range(start + 1, start + length):
            current.next = ListNode(i if not rand else random.randrange(start, end))
            current = current.next
        return node

    @classmethod
    def random(cls, length=5, **kwargs):
        return cls.create(length, rand=True, **kwargs)

    @classmethod
    def from_iter(cls, iterable):
        """从可迭代对象解析
        >>> ListNode.from_iter([1, 2, 3, 4]).to_number()
        1234
        """
        head = current = None
        for i in iterable:
            if current is None:
                current = head = ListNode(int(i))
            else:
                current.next = ListNode(int(i))
                current = current.next
        return head

    @classmethod
    def from_args(cls, *args):
        """ 从可变参数解析
        >>> ListNode.from_args(1,2,3,4).to_number()
        1234
        """
        return cls.from_iter(list(args))

    @classmethod
    def from_str(cls, values: str):
        """从 str 解析

        :param values: 视为每一位表示一个数字
        >>> ListNode.from_str('1234').to_number()
        1234
        """
        return cls.from_iter(values)

    @classmethod
    def from_num(cls, num: int):
        """从数字解析
        >>> ListNode.from_num(1234).to_number()
        1234
        """
        return cls.from_str(str(num))

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            lines = f.readlines()
            txt = ''.join(lines).replace('\n', '').replace('[', '').replace(']', '')
            return cls.from_iter(txt.split(','))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
