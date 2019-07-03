from leetcode import ListNode


class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        """
        可能会有相邻的相同元素
        可能需要移除头元素

        判断是否有连续的相同值，找到不相同的才连接
        >>> Solution().removeElements(ListNode.from_num(1123451),1).to_number()
        2345
        """
        # 找到 head
        while head and head.val == val:
            head = head.next
        # 开始移除
        cur = head
        while cur and cur.next:
            # 这和方式持有 next 了感觉没有 0203 中的优雅
            if cur.next.val == val:
                next = cur.next.next
                # 连续后移
                while next and next.val == val:
                    next = next.next
                cur.next = next
                cur = next
            else:
                # 不相等后移
                cur = cur.next
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
