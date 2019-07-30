from leetcode import ListNode


class Solution:
    """20190728"""

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        """
        前一题的扩展
        这样的 S(n) 是 O(k) 不是 O(1)
        >>> Solution().reverseKGroup(ListNode.from_num(12345),2).to_number()
        21435
        >>> Solution().reverseKGroup(ListNode.from_num(12345),3).to_number()
        32145
        """
        nodes = []
        n = 0
        pre = dummy = ListNode(0)
        dummy.next = p = head

        while True:
            while p and n < k:
                n += 1
                nodes.append(p)
                p = p.next
            if n == k:
                n = 0
                while nodes:
                    pre.next = nodes.pop()
                    pre = pre.next
                pre.next = p  # 将 pre 接上后续的结点
            else:
                return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
