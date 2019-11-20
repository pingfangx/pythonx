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

        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),1).to_number()
        1234
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),2).to_number()
        1235
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),5).to_number()
        2345
        """
        dummy = ListNode(0)
        dummy.next = head
        i = 1
        first = second = dummy
        while first.next:
            i += 1
            first = first.next
            if i > n + 1:  # 大于 n-1 两者都移动
                second = second.next
        second.next = second.next.next
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
