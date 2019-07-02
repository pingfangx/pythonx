from leetcode import ListNode


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        """
        迭代，如果 current==next 则继续取 next 取出后拼在 current 后
        每次不相等的时候都需要链接，实际已经链接了，是不需要的

        T(n)=O(n)
        S(n)=O(1)
        >>> Solution().deleteDuplicates(ListNode.create().append_tail(5)).trim()
        '12345'
        """
        current = head
        while current:
            next = current.next
            while next and current.val == next.val:
                next = next.next
            current.next = next
            current = next
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
