from leetcode import ListNode


class Solution:
    """20190727"""

    def swapPairs(self, head: ListNode) -> ListNode:
        """


            1   2       3      4
        cur p   p.next
        t=p.next.next       3
        cur.next=p.next     2
        p.next.next=p       2   1
        p.next=t            2   1   3


        >>> Solution().swapPairs(ListNode.from_num(1234)).to_number()
        2143
        >>> Solution().swapPairs(ListNode.from_num(12345)).to_number()
        21435
        """
        if not head:
            return head
        dummy = ListNode(0)
        dummy.next = head

        cur = dummy
        p = dummy.next
        while p and p.next:
            t = p.next.next  # 交换
            cur.next = p.next
            p.next.next = p
            p.next = t

            cur = p  # 后移
            p = p.next
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
