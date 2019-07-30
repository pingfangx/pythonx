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

        >>> Solution().reverseKGroup(ListNode.from_num(12345),2).to_number()
        21435
        >>> Solution().reverseKGroup(ListNode.from_num(12345),3).to_number()
        32145
        """
        dummy = ListNode(0)
        dummy.next = head

        pre = dummy
        right = head
        while True:
            i = 1
            while right and i < k:  # 后移 k-1 次，所以 i 初值为 1
                i += 1
                right = right.next
            if i == k and right is not None:  # 反转 left 到 right
                left = h = pre.next
                for _ in range(k - 1):  # 从 pre.next 开始反转 k-2 次
                    t = left.next.next  # 持有第三个
                    left.next.next = h  # 2接上头
                    h = left.next  # 此时 2 变为头
                    left.next = t  # 1接上3,left 不用移动，他的 next 已经变化

                pre.next = h  # pre 接上 头
                pre = left  # pre 置到最后一个
                right = left.next
            else:
                return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
