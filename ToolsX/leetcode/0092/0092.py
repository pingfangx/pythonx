from leetcode import ListNode


class Solution:
    """20190920"""

    def reverseBetween(self, head: ListNode, m: int, n: int) -> ListNode:
        """
        旋转一部分，考虑参数异常情况
        借助调试，居然过了，觉复有些复杂，去看讨论
        >>> Solution().reverseBetween(ListNode.from_num(12345),2,4).to_number()
        14325
        """
        if m >= n:
            return head

        dummy = ListNode(0)
        dummy.next = head
        i = 0
        pre, cur = dummy, dummy.next
        reverse_pre = reverse_end = None
        while cur:
            i += 1
            if i < m:
                pre = cur
                cur = cur.next
            elif i == m:  # 开始记录
                reverse_pre = pre
                reverse_end = cur
                t = cur.next
                cur.next = None
                pre = cur
                cur = t
            elif i < n:  # 翻转
                t = cur.next
                cur.next = pre
                pre = cur
                cur = t
            else:  # 结束翻转
                t = cur.next
                cur.next = pre
                reverse_pre.next = cur
                reverse_end.next = t
                break
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
