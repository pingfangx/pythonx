class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        路上思考了一下，有点难
        首先试一下没有使用 . 只使用 * 的情况
        递归时会创建多个字符串，占用更多空间，但是为了便于理解和简化操作，还是直接截取

        1
        加上 . 补充判断

        2
        写了辣么多，答案那么简单，感觉，哎
        >>> Solution().isMatch('aaa','ab*a*c*a')
        True
        >>> Solution().isMatch('','')
        True
        >>> Solution().isMatch('a','')
        False
        >>> Solution().isMatch('','a')
        False
        >>> Solution().isMatch('','.')
        False
        >>> Solution().isMatch('','.*')
        True
        >>> Solution().isMatch('a','*')
        False
        >>> Solution().isMatch('a','a*')
        True
        >>> Solution().isMatch('abbc','ab*c*')
        True
        >>> Solution().isMatch('a','.')
        True
        >>> Solution().isMatch('ab','a.')
        True
        >>> Solution().isMatch('ab','.*')
        True
        >>> Solution().isMatch('abc','a.*')
        True
        >>> Solution().isMatch('aab','c*a*b')
        True
        >>> Solution().isMatch('aaa','ab*a*c*a')
        True
        """
        if not p:
            return not s

        # 第一个是否匹配
        first_match = bool(s) and p[0] in [s[0], '.']

        if len(p) >= 2 and p[1] == '*':
            return self.isMatch(s, p[2:]) or first_match and self.isMatch(s[1:], p)
        else:
            # 第一个匹配，继续
            return first_match and self.isMatch(s[1:], p[1:])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
