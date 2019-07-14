from leetcode import ListNode


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """链表相加，值为倒序
        要注意的就是找到位数差异（实际不用，因为倒序，前面的就是低位）和补上进位
        比如
        123
        12345
        之前的两个指针遍历

        O(max(m,n))
        迭代最长的链表次

        空间复杂度
        O(max(m,n))

        因为不是就地进行的，需要分配整个结果链表
        >>> l1=ListNode.from_num(12)
        >>> l2=ListNode.from_num(9999)
        >>> Solution().addTwoNumbers(l1,l2).to_array()
        [0, 2, 0, 0, 1]
        >>> Solution().addTwoNumbers(ListNode.from_num(98),ListNode.from_num(1)).to_array()
        [0, 9]
        """
        # 命名错误，不是余数
        remainder = 0
        p = dummy = ListNode(0)  # 使用 dump 避免最前面的判断和首次赋值
        while l1 and l2:
            t = l1.val + l2.val + remainder
            # 可以改用 divmod
            v, remainder = t % 10, t // 10  # 余数每次都得新赋值
            p.next = ListNode(v)
            p = p.next  # p 也要后移
            l1 = l1.next
            l2 = l2.next
        # 移动结束，追加剩余的
        if l1:
            p.next = l1
        if l2:
            p.next = l2
        # 追加后，如果有值，判断是否需要进位
        # 这里使用 next 因为要持有 p 后面要添加进位
        while p.next:
            t = p.next.val + remainder
            v, remainder = t % 10, t // 10
            p.next.val = v
            if remainder == 0:
                # 没有进位，提前结束，后面也不需要再判断，也不需要再后移指针
                break
            p = p.next
        # 剩余部分追加结束，或者没有追加，都要判断余数
        if remainder:
            p.next = ListNode(remainder)
        return dummy.next  # 因为最前面添加了 dummy


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
