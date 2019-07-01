from leetcode import ListNode


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        """
        该解法是参照
        https://leetcode.com/problems/reverse-linked-list/discuss/323687/9-lines-java-code.-time-less-than-100-space-less-than-almost-100
            ListNode tail = null;
            ListNode temp;
            while (head != null) {
                temp = head.next;
                head.next = tail;
                tail = head;
                head = temp;
            }
            return tail;
        >>> Solution().reverseList(ListNode.create())
        5 -> 4 -> 3 -> 2 -> 1

        >>> Solution().reverseList(ListNode.create(0))

        >>> a=1
        >>> b=2
        >>> c=3
        >>> a,b,c=b,c,a
        >>> print(a,b,c)
        2 3 1
        """
        pre = None
        while head:
            # 断开并指向前 pre
            # pre 后移，head 后移
            head.next, pre, head = pre, head, head.next
        return pre


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
