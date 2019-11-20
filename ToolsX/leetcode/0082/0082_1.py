from leetcode import ListNode


class Solution:
    """20190912"""

    def deleteDuplicates(self, head: ListNode) -> ListNode:
        """
        好久没有链表，还是链表亲切一些，可能是因为链表的题不会太难
        题目要求的是如果重复就删除，而不是只留一个


        0   1   2   3   3   4   4   5
        pre cur nxt 不相等，后移
            pre cur nxt
                pre cur nxt 相等，后移 nxt
                pre cur     nxt，将 pre.next 连接到 nxt，同时移动 cur 和 nxt
                pre         cur nxt，继续判断 cur 和 nxt

        1
        不需要持有 next
        0   1   2   3   3   4   4   5
        pre cur 后移
            pre cur
                pre cur 相等，后移 cur
                pre     cur，将 pre.next 指向 cur.next，同时 cur 也后移
                pre         cur，同样相等，后移 cur
                pre             cur，pre.next 指向 5，后移 cur
                pre                 cur，结束，后移
                                    pre cur
        >>> Solution().deleteDuplicates(ListNode.from_num(1233445)).to_number()
        125
        """
        dummy = ListNode(0)
        dummy.next = head
        pre, cur = dummy, head
        while cur:
            if cur.next and cur.val == cur.next.val:
                while cur.next and cur.val == cur.next.val:  # 后移
                    cur = cur.next
                pre.next = cur.next  # 如果有效，pre 会移动到 pre.next，否则，会重新赋值 pre.next
                cur = cur.next
            else:  # 不相等，后移
                pre = pre.next
                cur = cur.next
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
