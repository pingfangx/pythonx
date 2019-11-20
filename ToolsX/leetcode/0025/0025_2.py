from leetcode import ListNode


class Solution:
    """20190728"""

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        """
        前一题的扩展
        这样的 S(n) 是 O(k) 不是 O(1)

        1
        记数反转


        dummy       1       2       3       4
        pre         right
        pre                 right
        pre                         right               执行反转

                    left    left.next t
                    2       1       3       4
                            left    left.next t
        dummy       2       1       3       4
                            pre     right
                            pre             right

        太乱了，太难理解了，不调试都无法正常运行，参考答案重新修改

        2
        参考（别人的）答案重写

        >>> Solution().reverseKGroup(ListNode.from_num(12345),2).to_number()
        21435
        >>> Solution().reverseKGroup(ListNode.from_num(12345),3).to_number()
        32145
        """
        dummy = jump = ListNode(-1)
        dummy.next = head
        left = right = head
        while True:
            count = 0
            while right and count < k:  # 移动 k 次，当结束时，k 位于子链的后一结点，也就是下一子链的第一位
                right = right.next
                count += 1
            if count == k:
                # 交换
                pre = right  # 首次交换应该接到下一结点
                cur = left
                for _ in range(k):
                    nxt = cur.next  # 取第2个暂存用于后移
                    cur.next = pre  # 1连接h
                    pre = cur  # 置为 pre
                    cur = nxt  # 后移
                # 连接
                jump.next = pre
                jump = left  # left 是子序列的第一位，反转后为最后一位
                left = right  #
            else:
                return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
