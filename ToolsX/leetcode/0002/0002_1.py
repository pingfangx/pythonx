from leetcode import ListNode


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """链表相加，值为倒序
        要注意的就是找到位数差异（实际不用，因为倒序，前面的就是低位）和补上进位
        比如
        123
        12345
        之前的两个指针遍历

        1
        答案中结出的方法，可以判断 l1 or l2，在一个循环中完成，不要后面拼接给自己带来麻烦

        >>> l1=ListNode.from_num(12)
        >>> l2=ListNode.from_num(9999)
        >>> Solution().addTwoNumbers(l1,l2).to_array()
        [0, 2, 0, 0, 1]
        >>> Solution().addTwoNumbers(ListNode.from_num(98),ListNode.from_num(1)).to_array()
        [0, 9]
        """
        carry = 0
        p = dummy = ListNode(0)  # 使用 dump 避免最前面的判断和首次赋值
        while l1 or l2:
            x = 0 if not l1 else l1.val
            y = 0 if not l2 else l2.val
            t = x + y + carry
            v, carry = t % 10, t // 10  # 余数每次都得新赋值
            p.next = ListNode(v)
            p = p.next  # p 也要后移
            l1 = l1 if not l1 else l1.next
            l2 = l2 if not l2 else l2.next
        if carry:
            p.next = ListNode(carry)
        return dummy.next  # 因为最前面添加了 dummy


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
