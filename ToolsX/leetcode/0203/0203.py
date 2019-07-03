from leetcode import ListNode


class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        """
        可能会有相邻的相同元素
        可能需要移除头元素

        先找出 head
        然后持有 cur 判断 next
        如果 next.val==val 则将 next.next 接到 cur 后
        这种便于理解，但是如果有连续相同 next ，可能会浪费时间在连接上

        >>> Solution().removeElements(ListNode.from_num(1123451),1).to_number()
        2345
        """
        # 找到 head
        while head and head.val == val:
            head = head.next
        # 开始移除
        cur = head
        while cur and cur.next:
            if cur.next.val == val:
                # 如果相等，连接 next.next，不移动 cur 继续判断
                cur.next = cur.next.next
            else:
                # 不相等则后移 cur
                cur = cur.next
        return head


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
