from leetcode import ListNode


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        """
        首先要遍历一遍获取长度
        如果要时间，那就用 hash map 记录结点位置
        如果要空间，那就再遍历一遍
        注意删除 head
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),1).to_number()
        1234
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),2).to_number()
        1235
        >>> Solution().removeNthFromEnd(ListNode.from_num(12345),5).to_number()
        2345
        """
        if not head:
            return head
        node = head
        length = 1
        while node.next:
            length += 1
            node = node.next
        if length < n:
            return head
        elif length == n:
            return head.next
        else:  # 删除某一个结点
            # 比如 length 5,n=4，需要删除第 2 个，移动 0 次
            i = length - n - 1
            node = head
            while i > 0:
                i -= 1
                node = node.next
            node.next = node.next.next
            return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
