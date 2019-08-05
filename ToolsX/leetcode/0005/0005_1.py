class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        一开始没有好的方法，就遍历吧，向左右扩展

        1
        答案中提示，反转是不可行的，因为可能首尾相同，但是中间不相同
        但是可以判断索引

        在答案四中，与我们 0005 的算法一致，但是可以优化
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

        def expand(left, right):
            while left >= 0 and right < n and s[left] == s[right]:  # 前后相等
                left -= 1
                right += 1
            return right - left + 1 - 2  # 因为退出时不满足循环条件，所以-2

        for i in range(0, n):
            len1 = expand(i, i)
            len2 = expand(i, i + 1)
            cur_max = max(len1, len2)
            if max_len < cur_max:
                max_len = cur_max
                # 比如 3 个，左右各一个，减去 2//2
                # 比如 4 个，左右还是各一个，减去 3//2
                max_start = i - (cur_max - 1) // 2

        return s[max_start:max_start + max_len]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
