from leetcode import ListNode


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        """
        >>> Solution().reverseList(ListNode.create())
        5 -> 4 -> 3 -> 2 -> 1

        >>> Solution().reverseList(ListNode.create(0))

        """
        if not head:
            return head
        # 持有 pre 和 current，通过 current 获取 next
        pre = head
        current = pre.next
        # 因为链首变为链尾了，要置空
        pre.next = None

        while current:
            # 持有 next
            next = current.next
            # 接上 pre
            current.next = pre

            # 移动指针
            pre = current
            current = next

        return pre


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
