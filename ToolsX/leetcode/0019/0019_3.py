from leetcode import ListNode


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        """
        首先要遍历一遍获取长度
        如果要时间，那就用 hash map 记录结点位置
        如果要空间，那就再遍历一遍
        注意删除 head

        1
        答案中提到删除第 length-n+1 个结点，这样比较好理解

        2
        两个指针一起移动，维持 n+1 的间距
        比如倒数第一个，应该停在倒数第2个处，相差两个，即 n+1 个

        3
        讨论中的实现比较 pythonic

        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),1).to_number()
        1234
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),2).to_number()
        1235
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),5).to_number()
        2345
        """
        fast = head
        for _ in range(n):  # 认为n<=length，[0,n)移动了 n 步，形成了 n+1 的间距
            fast = fast.next
        if not fast:  # 到达末尾，删除头
            return head.next

        slow = head
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
