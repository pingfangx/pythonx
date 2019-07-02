from leetcode import ListNode


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        """
        current 不断后移
        如果有相等的，找到最后一个，拼接

        T(n)=O(n)
        S(n)=O(1)
        >>> Solution().deleteDuplicates(ListNode.create().append_tail(5)).trim()
        '12345'
        """
        if not head:
            # 不提前返回则需要在 while 中加判断
            return head

        current = head
        while current.next:
            # 不相待继续迭代
            if current.val != current.next.val:
                # current 后移
                current = current.next
                continue
            # 如果相等，不断后移 current
            while current.val == current.next.val:
                current.next = current.next.next
                # 手动判断，不加到 while 中，因为 while 第一次不需要判断
                if not current.next:
                    break
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
