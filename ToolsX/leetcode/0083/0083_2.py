from leetcode import ListNode


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        """
        https://leetcode.com/problems/remove-duplicates-from-sorted-list/discuss/28621/Simple-iterative-Python-6-lines-60-ms
        其实 0 中已经接近了，但是不需要 next

        T(n)=O(n)   判断是否相等
        S(n)=O(1) 不需要多余空间
        >>> Solution().deleteDuplicates(ListNode.create().append_tail(5)).trim()
        '12345'
        """
        current = head
        while current:
            while current.next and current.val == current.next.val:
                current.next = current.next.next  # 跳过相等的
            current = current.next  # 后移
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
