from leetcode import ListNode


class Solution:
    """20190915"""

    def partition(self, head: ListNode, x: int) -> ListNode:
        """
        思路就是记录两个链表
        和答案一致，但是答案标明的是 Approach 1，可能还有别的解法
        否则就如评论所说，这应该是 easy 难度，我也就只能做做 easy 难度了 T...T
        >>> Solution().partition(ListNode.from_num(143252),3).to_number()
        122435
        """
        p1 = dummy1 = ListNode(0)
        p2 = dummy2 = ListNode(0)
        p = head
        while p:
            if p.val < x:  # 前
                p1.next = p
                p1 = p
            else:
                p2.next = p
                p2 = p
            p = p.next
        p1.next = None  # 多余
        p2.next = None
        p1.next = dummy2.next
        return dummy1.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
