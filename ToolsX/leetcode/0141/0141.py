from leetcode import ListNode


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        """
        最最浅显的方法，也就是收集整个链
        但是
        S(n)=O(n)
        不符合期望的 O(1)
        >>> l=ListNode.create()
        >>> Solution().hasCycle(l.append_tail(l))
        True
        """
        nodes = []
        while head:
            if head in nodes:
                return True
            nodes.append(head)
            head = head.next
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
