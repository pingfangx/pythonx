# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        return f'{self.val}' + ('' if not self.next else f' -> {self.next}')

    def __repr__(self):
        return self.__str__()

    @classmethod
    def create(cls, length=5):
        if length == 0:
            return None
        node = ListNode(1)
        if length == 1:
            return node
        current = node
        for i in range(2, length + 1):
            current.next = ListNode(i)
            current = current.next
        return node
