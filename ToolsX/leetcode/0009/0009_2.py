class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        想到几种
        一是收集数字，再判断
        二是通过弹出数字的时候就反转
        三是求出数字位数

        2
        1 中的思路已经接近了，甚至 %10 都想到了

        T(n)=O(log 10(n))
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
        if x <= 0 or x % 10 == 0:
            return False
        reverse = 0
        while x > reverse:
            reverse = reverse * 10 + x % 10
            x //= 10
        return reverse == x or reverse // 10 == x


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
