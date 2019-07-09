from leetcode import ListNode


class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        """
        最笨的思路，还是收集，取中间点，再判断
        但是 T(n)=O(n),S(n)=O(n)

        下列算法以时间换空间 T(n)=O(n^2),S(n)=O(1)
        先算出长度，从中间分开，right 向右，left 从中间向左，依次比较
        但是提交直接超时……
        >>> Solution().isPalindrome(None)
        True
        >>> Solution().isPalindrome(ListNode.from_num(1))
        True
        >>> Solution().isPalindrome(ListNode.from_num(12321))
        True
        >>> Solution().isPalindrome(ListNode.from_num(123321))
        True
        """
        length = 0
        p = head
        while p:
            length += 1
            p = p.next
        if length <= 1:
            return True
        # length 3 half 2
        # 后续的 half i j 都从 0 开始
        half = int(length / 2 + 0.5)

        # 取到 右侧
        right = head
        i = 0
        while i < half:
            i += 1
            right = right.next

        # 开始判断
        while i < length:
            # 算 index 求出 left
            index = length - i - 1
            left = head
            j = 0
            while j < index:
                j += 1
                left = left.next
            if right.val != left.val:
                return False
            i += 1
            right = right.next
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
