from leetcode import ListNode


class Solution:
    def deleteNode(self, node: ListNode) -> None:
        """
        hum hum, I can't understand the mean of the question until I saw the solution.
        看了答案终于知道是什么意思了，意思当链表要删除某个结点时调用的方法，参数不是链表，而是要删除的结点
        因为要删除当前，无法获得 pre，所以只能将当前置为下一个，然后删除下一个
        >>> l=ListNode.create()
        >>> Solution().deleteNode(l.next)
        >>> l.to_number()
        1345
        """
        node.val = node.next.val
        node.next = node.next.next

        # node.val, node.next = node.next.val, node.next.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
