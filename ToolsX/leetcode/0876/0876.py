from leetcode import ListNode


class Solution:
    def middleNode(self, head: ListNode) -> ListNode:
        """
        之前用过 slow fast 就很简单了
        奇数时，fast 到达尾部，slow 到达正中间
        偶数时，fast 到达尾部的 next ，slow 到达中间偏右
        >>> Solution().middleNode(None)

        >>> Solution().middleNode(ListNode.from_num(1)).val
        1
        >>> Solution().middleNode(ListNode.from_num(123)).val
        2
        >>> Solution().middleNode(ListNode.from_num(1234)).val
        3
        """
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
