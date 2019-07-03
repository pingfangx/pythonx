class Node:
    def __init__(self, val):
        self.val = val
        self.pre = None
        self.next = None


class MyLinkedList:
    """
    持有一个 cur
    然后每个结点有 pre 和 next
    但是实际处理中需要注意在添加和删除第 0  个（即 head）时需要特殊处理
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.cur = None
        self.size = 0

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        node = self.get_node(index)
        if node:
            return node.val
        else:
            return -1

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        # 在前面添加
        self.add_node_before(self.cur, val)
        # 将 cur 前移
        self.cur = self.cur.pre

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        # 在前面添加
        self.add_node_before(self.cur, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        if index < 0:
            # 提交时有该测试
            index = 0
        if index == self.size:
            # 等于 size 时添加在最后
            self.addAtTail(val)
        else:
            node = self.get_node(index)
            if node:
                self.add_node_before(node, val)
            if index == 0:
                # 添加删除链首时，需要特殊处理
                self.cur = self.cur.pre

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        node = self.get_node(index)
        if node:
            if index == 0:
                # 添加删除链首时，需要特殊处理
                self.cur = self.cur.next
            self.delete_node(node)

    def add_node_before(self, cur, val):
        if self.size == 0:
            self.cur = Node(val)
            self.cur.pre = self.cur
            self.cur.next = self.cur
            self.size += 1
        else:
            node = Node(val)
            self.size += 1

            pre = cur.pre
            cur.pre = node
            node.next = cur

            pre.next = node
            node.pre = pre

    def delete_node(self, node):
        self.size -= 1
        if self.size == 0:
            self.cur = None
        else:
            node.pre.next = node.next
            node.next.pre = node.pre

    def get_node(self, index: int):
        if index < 0 or index >= self.size:
            return None
        node = self.cur
        i = 0
        while i < index:
            i += 1
            node = node.next
        return node

    def __str__(self):
        s = ''
        p = self.cur
        for i in range(self.size):
            s += ('' if i == 0 else ' -> ') + f'{p.val}'
            p = p.next
        return s

    def __repr__(self):
        return self.__str__()


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)

def test_run(methods, params):
    linklist = MyLinkedList()
    for i, method in enumerate(methods):
        if i == 0:
            print('MyLinkedList()')
            continue
        param = params[i]
        length = len(param)
        if length == 1:
            r = getattr(linklist, method)(param[0])
            print(f'{method}({param[0]}):{r},{linklist}')
        elif length == 2:
            r = getattr(linklist, method)(param[0], param[1])
            print(f'{method}{(param[0], param[1])}:{r},{linklist}')


if __name__ == '__main__':
    test_run(["MyLinkedList", "addAtIndex", "get", "deleteAtIndex"],
             [[], [-1, 0], [0], [-1]])
