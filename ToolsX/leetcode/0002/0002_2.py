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

        2
        讨论中的优化，不需要 x,y

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
            if l1:
                carry += l1.val
                l1 = l1.next
            if l2:
                carry += l2.val
                l2 = l2.next
            carry, v = divmod(carry, 10)
            p.next = ListNode(v)
            p = p.next
        if carry:
            p.next = ListNode(carry)
        return dummy.next


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
