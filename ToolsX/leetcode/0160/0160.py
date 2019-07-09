from leetcode import ListNode


class Solution:

    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        """
        每个结点都有一个 parent，如果某个结点有两个 parent，则说明是交点
        但是这样不行呀

        getIntersectionNode_store
        记录整个 A 链表，再判断 B，这样的话 S(n)=O(n)

        getIntersectionNode_iter
        两层迭代，依次判断，但这样的话 T(n)=O(n^2)
        这两种方案都失败了……
        >>> la=ListNode.create()
        >>> lb=ListNode.create()
        >>> lb.get_tail().next=la.next
        >>> Solution().getIntersectionNode_store(la,lb).trim()
        '2345'
        >>> Solution().getIntersectionNode_iter(la,lb).trim()
        '2345'
        """

    def getIntersectionNode_store(self, headA: ListNode, headB: ListNode) -> ListNode:
        """
        S(n)=O(n)
        """
        nodes = []
        while headA:
            nodes.append(headA)
            headA = headA.next
        while headB:
            if headB in nodes:
                return headB
            headB = headB.next
        return None

    def getIntersectionNode_iter(self, headA: ListNode, headB: ListNode) -> ListNode:
        """ T(n)=O(n^2)"""
        i = headA
        while i:
            j = headB
            while j:
                if i is j:
                    return i
                j = j.next
            i = i.next
        return None


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
