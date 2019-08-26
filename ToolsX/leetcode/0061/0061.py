from leetcode import ListNode


class Solution:
    """20190826"""

    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        """
        需要先求出长度

        1
        在求长度的过程中，已经到达了末尾
        >>> Solution().rotateRight(ListNode.from_num(12345),2).to_number()
        45123
        >>> Solution().rotateRight(ListNode.from_str('012'),4).to_number()
        201
        """
        if not head:
            return head
        p = head
        n = 1
        while p.next:
            n += 1
            p = p.next
        if n <= 1:
            return head

        k = k % n
        if k == 0:
            return head

        p.next = head  # 接成环

        i = 1
        p = head  # 要断开，p 必须为断开处的前一个
        while i <= (n - k - 1):  # 5-2=3，前面 3 个，需要移动 2 步，移动到 i==3
            i += 1
            p = p.next
        new_head = p.next
        p.next = None  # p 变为链尾
        return new_head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
