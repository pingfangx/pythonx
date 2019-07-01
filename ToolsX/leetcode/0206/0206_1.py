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

        """
        pre = None
        while head:
            # 断开并指向前一个
            next = head.next
            # 移动指针
            head.next, pre, head = pre, head, next
        # pre 是 head 的前一个，退出循环时，head 为空，所以是返回 pre
        return pre


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
