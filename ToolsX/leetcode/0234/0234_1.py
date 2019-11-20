from leetcode import ListNode


class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        """
        学习之后，我们知道可以反转一个链表
        T(n)=O(n)
        >>> Solution().isPalindrome(None)
        True
        >>> Solution().isPalindrome(ListNode.from_num(1))
        True
        >>> Solution().isPalindrome(ListNode.from_num(12321))
        True
        >>> Solution().isPalindrome(ListNode.from_num(123321))
        True
        """
        if not head or not head.next:
            return True
        slow = fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        # reverse slow
        pre = slow
        right = slow.next
        pre.next = None
        while right:
            nxt = right.next
            right.next = pre

            pre = right
            right = nxt

        # compare
        left = head
        right = pre
        while right:
            if right.val != left.val:
                return False
            right = right.next
            left = left.next
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
