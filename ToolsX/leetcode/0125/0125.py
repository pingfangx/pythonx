import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        """

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
        # 忽略标点
        s = re.sub(r'\W', '', s).lower()
        # 中点
        half = len(s) // 2
        # 最后 half 个，反转
        return True if half < 1 else s[:half] == s[-half:][::-1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
