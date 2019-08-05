from leetcode import ListNode


class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        """
        可能会有相邻的相同元素
        可能需要移除头元素

        看了别人的解法，其实是不需要找出 head 的，返回之前处理即可
        甚至还有添加一个 dummy  head 的，感觉没有必要
        >>> Solution().removeElements(ListNode.from_num(1123451),1).to_number()
        2345
        """
        cur = head
        while cur and cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head if not head or head.val != val else head.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
