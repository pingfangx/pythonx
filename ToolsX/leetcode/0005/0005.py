class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        一开始没有好的方法，就遍历吧，向左右扩展
        >>> Solution().longestPalindrome('')
        ''
        >>> Solution().longestPalindrome('a')
        'a'
        >>> Solution().longestPalindrome('ac')
        'a'
        >>> Solution().longestPalindrome('babad')
        'bab'
        >>> Solution().longestPalindrome('abcdeff')
        'ff'
        >>> Solution().longestPalindrome('aabcdef')
        'aa'
        """
        n = len(s)
        if n <= 1:  # 因为后面是成对扩展，1 无法处理
            return s
        max_start = 0
        max_len = 0
        for i in range(0, n - 1):  # 从 0 开始，因为偶数要取到当前
            # 奇数扩展
            left = i - 1
            right = i + 1
            cur_start = 0
            cur_max = 1  # 包含当前位置
            while left >= 0 and right < n and s[left] == s[right]:  # 前后相等
                cur_start = left
                left -= 1
                right += 1
                cur_max += 2
            if max_len < cur_max:
                max_len = cur_max
                max_start = cur_start

            # 偶数扩展
            left = i
            right = i + 1
            cur_start = 0
            cur_max = 0
            while left >= 0 and right < n and s[left] == s[right]:  # 前后相等
                cur_start = left
                left -= 1
                right += 1
                cur_max += 2
            if max_len < cur_max:
                max_len = cur_max
                max_start = cur_start
        return s[max_start:max_start + max_len]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
