from leetcode import ListNode


class Solution:
    def deleteNode(self, head: ListNode, node: ListNode) -> None:
        """
        需要持有 pre，要判断 next.next
        当 cur.next.next 为空时，设 pre.next=cur.next
        >>> l=ListNode.create()
        >>> Solution().deleteNode(l,ListNode(4))
        >>> l.to_number()
        1235
        >>> l=ListNode.from_num(1123114)
        >>> Solution().deleteNode(l,ListNode(1))
        >>> l.to_number()
        234
        """
        while head and head.val == node.val:
            head = head.next
        pre = head
        cur = head
        while cur:
            if cur.val == node.val:
                # 如果相等则连到下一个
                pre.next = cur.next

            pre, cur = cur, cur.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
