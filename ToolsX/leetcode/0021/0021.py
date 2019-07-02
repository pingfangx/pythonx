from leetcode import ListNode


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        需要两个变量，一个记录 head，一个记录 min 并不断后移
        注意判断移动前是否有空链表，和移动结束后是否有剩余结点
        >>> Solution().mergeTwoLists(ListNode.create(),ListNode.create(start=2)).trim()
        '1223344556'
        >>> Solution().mergeTwoLists(ListNode.create(start=2),ListNode.create()).trim()
        '1223344556'
        """

        if not l1:
            # 也包含 l1 l2 均为空，此时返回空
            return l2
        if not l2:
            return l1

        # 求出 min 指针，记录 head
        # 要注意记录了 min 同时要移动 l1 或 l2
        if l1.val < l2.val:
            min = l1
            l1 = l1.next
        else:
            min = l2
            l2 = l2.next
        head = min
        while l1 and l2:
            if l1.val < l2.val:
                min.next = l1
                l1 = l1.next
            else:
                min.next = l2
                l2 = l2.next
            min = min.next

        # 一定要加上最后剩下的
        if not l1:
            l1 = l2
        while l1:
            min.next = l1
            l1 = l1.next
            min = min.next
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
