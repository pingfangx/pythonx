class Solution:
    def isPalindrome(self, s: str) -> bool:
        """

        1
        不用正则，手动判断
        注意忽略大小写
        >>> Solution().isPalindrome('')
        True
        >>> Solution().isPalindrome('a')
        True
        >>> Solution().isPalindrome('aa')
        True
        >>> Solution().isPalindrome('aba')
        True
        >>> Solution().isPalindrome('A man, a plan, a canal: Panama')
        True
        """
        l = 0
        r = len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
