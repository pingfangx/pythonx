from leetcode import ListNode


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        """
        fast 每次两步，slow 每次一步，进入环后，fast 绕一圏后肯定相遇
        https://leetcode.com/problems/linked-list-cycle/discuss/44489/O(1)-Space-Solution/154560
        喜欢
        S(n)=O(1)
        >>> l=ListNode.create()
        >>> Solution().hasCycle(l.append_tail(l))
        True
        """
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if id(slow) == id(fast):
                return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
