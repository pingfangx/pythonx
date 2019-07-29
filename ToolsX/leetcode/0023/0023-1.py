from queue import PriorityQueue
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
        p = dummy = ListNode(0)
        q = PriorityQueue()
        for i in lists:
            if i:
                q.put((i.val, i))  # 以值为优先级
        while not q.empty():
            val, node = q.get()  # 取出的即为最小的
            p.next = ListNode(val)
            p = p.next
            node = node.next
            if node:
                q.put((node.val, node))  # 如果还有 next 加入队列
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
