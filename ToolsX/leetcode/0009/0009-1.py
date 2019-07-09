class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        想到几种
        一是收集数字，再判断
        二是通过弹出数字的时候就反转
        三是求出数字位数

        >>> Solution().isPalindrome(121)
        True
        >>> Solution().isPalindrome(-121)
        False
        >>> Solution().isPalindrome(100)
        False
        >>> Solution().isPalindrome(0)
        True
        """
        if x == 0:
            return True
        # 如果以 0 结尾肯定不是回文数，并且会影响后面 reverse 的判断，所以特殊处理
        if x < 0 or x % 10 == 0:
            return False
        reverse = 0
        while x:
            # 奇数情况，比如 121 第二轮取了 2 得到 12 与 12 比较
            reverse = reverse * 10 + x % 10
            if reverse == x:
                return True
            x //= 10
            # 偶数情况，比如 2332，第二轮得到 23 与 23 比较
            if reverse == x:
                return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
