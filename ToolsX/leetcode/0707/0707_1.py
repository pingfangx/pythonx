class MyLinkedList:
    """用数组偷懒"""

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.data = []
        self.length = 0

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        if index < 0 or index >= self.length:
            return -1
        return self.data[index]

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        self.addAtIndex(self.length, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        if index > self.length:
            return
        if index < 0:
            index = 0
        self.data.insert(index, val)
        self.length += 1

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        if index < 0 or index >= self.length:
            return
        self.data[index:] = self.data[index + 1:]
        self.length -= 1

    def __str__(self):
        return str(self.data)

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
    test_run(
        ["MyLinkedList", "addAtHead", "addAtIndex", "get", "get", "get"],
        [[], [1], [1, 2], [1], [0], [2]]
    )
