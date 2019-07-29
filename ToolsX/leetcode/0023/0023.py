from typing import List

from leetcode import ListNode


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        """
        既然是已排序的，只需要依次比较就好了
        超时

        该方法是答案中的方法2
        答案中更暴力，直接收集所以结点，然后进行排序。


        >>> Solution().mergeKLists([ListNode.from_num(145),ListNode.from_num(134),ListNode.from_num(26)]).to_number()
        11234456
        """
        dummy = ListNode(0)
        p = dummy
        n = len(lists)
        while True:
            min_node = -1
            for i in range(n):
                if lists[i] is None:
                    continue
                if min_node == -1 or lists[i].val < lists[min_node].val:
                    min_node = i
            # 找出最小的结点
            if min_node == -1:  # 没有更多结点
                return dummy.next
            else:
                p.next = lists[min_node]
                p = p.next
                lists[min_node] = lists[min_node].next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
