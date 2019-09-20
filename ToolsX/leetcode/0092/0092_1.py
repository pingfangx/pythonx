from leetcode import ListNode


class Solution:
    """20190920"""

    def reverseBetween(self, head: ListNode, m: int, n: int) -> ListNode:
        """
        旋转一部分，考虑参数异常情况
        借助调试，居然过了，觉复有些复杂，去看讨论

        1
        https://leetcode.com/problems/reverse-linked-list-ii/discuss/30709/Talk-is-cheap-show-me-the-code-(and-DRAWING)

        0   1   2   3   4   5
        p
            p   移动到移动的前面
                tail
            交换 p.next=tail.next     1 连上 3
                tail.next=tail.next.next    2 连上 4
                p.next.next=t           3 连上 2
        0   1   3   2   4   5
            p       tail
            t=p.next                记录 3
            p.next=tail.next        1 连上 4
            tail.next=tail.next.next 2 连上 5
            p.next.next=t            4 连上 3
        0   1   4   3   2   5
        >>> Solution().reverseBetween(ListNode.from_num(12345),2,4).to_number()
        14325
        """
        if not head or m >= n:
            return head
        p = dummy = ListNode(0)
        dummy.next = head

        for _ in range(m - 1):
            p = p.next

        tail = p.next  # p 最初移动到要交换位置的前面，tail 是第一个要交换的元素
        for _ in range(n - m):
            t = p.next
            p.next = tail.next
            tail.next = tail.next.next
            p.next.next = t
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
