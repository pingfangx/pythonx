from typing import List

from leetcode import ListNode


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        """
        既然是已排序的，只需要依次比较就好了
        超时

        该方法是答案中的方法2
        答案中更暴力，直接收集所以结点，然后进行排序。

        1
        需要重写 __lt__


        >>> Solution().mergeKLists([ListNode.from_num(145),ListNode.from_num(134),ListNode.from_num(26)]).to_number()
        11234456
        """
        nodes = []
        for i in lists:
            while i:
                nodes.append(i.val)
                i = i.next
        nodes.sort()
        p = dummy = ListNode(0)
        for i in nodes:
            p.next = ListNode(i)
            p = p.next
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
