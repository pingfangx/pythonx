from leetcode import ListNode


class Solution:

    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        """
        https://leetcode.com/problems/intersection-of-two-linked-lists/discuss/49798/Concise-python-code-with-comments
        思路真好啊，如果有交点，将两个链表连起来，每次 next，则第二轮肯定会相遇
        因为如果两链合成一链，最后一部分是相同的，就会在相同的那个点相等
        >>> la=ListNode.create()
        >>> lb=ListNode.create()
        >>> lb.get_tail().next=la.next
        >>> Solution().getIntersectionNode(la,lb).trim()
        '2345'
        """
        if not headA or not headB:
            return None
        pa = headA
        pb = headB
        while pa is not pb:
            pa = headB if pa is None else pa.next
            pb = headA if pb is None else pb.next
        return pa


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
