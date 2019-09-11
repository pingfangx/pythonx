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

        >>> Solution().deleteDuplicates(ListNode.from_num(1233445)).to_number()
        125
        """
        if not head:  # 因为后面要取 head.next 所以提前判断
            return head
        dummy = ListNode(0)
        dummy.next = head
        pre, cur, nxt = dummy, head, head.next
        while cur and nxt:
            if cur.val != nxt.val:  # 不相等，后移
                pre.next = cur
                pre, cur, nxt = cur, nxt, nxt.next
            else:
                while nxt and cur.val == nxt.val:  # 相等，查找 nxt
                    nxt = nxt.next
                pre.next = nxt
                if nxt:
                    cur, nxt = nxt, nxt.next
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
