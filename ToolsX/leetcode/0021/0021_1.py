from leetcode import ListNode


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        https://leetcode.com/problems/merge-two-sorted-lists/discuss/9735/Python-solutions-(iteratively-recursively-iteratively-in-place).
        思路简单，next 为后续合并
        >>> Solution().mergeTwoLists(ListNode.create(),ListNode.create(start=2)).trim()
        '1223344556'
        >>> Solution().mergeTwoLists(ListNode.create(start=2),ListNode.create()).trim()
        '1223344556'
        """
        if not l1:
            # 也包含 l1 l2 均为空，此时返回空
            return l2
        if not l2:
            return l1
        if l1.val < l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
