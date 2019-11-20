class Solution:
    """20190811"""

    def isMatch(self, s: str, p: str) -> bool:
        """
        匹配 ? 和 *
        又是各种判断

        >>> Solution().isMatch('ho','**ho')
        True
        >>> Solution().isMatch('cb','?a')
        False
        >>> Solution().isMatch('adceb','*a*b')
        True
        >>> Solution().isMatch('adceb','a*b')
        True
        >>> Solution().isMatch('acdcb','a*c?b')
        False
        """
        if not s and not p:
            return True
        if not p:
            return False
        if not s:
            return p.strip('*') == ''
        last = p[-1]
        if last == '?':  # 匹配任意字符
            return self.isMatch(s[:-1], p[:-1])
        elif last == '*':  # 任意多次
            if len(p) == 1:  # * 匹配任意字符
                return True
            else:
                for i in range(len(s) + 1):  # 匹配任意数量
                    if self.isMatch(s[0:i], p[:-1]):
                        return True
                return False
        else:  # 字符
            return s[-1] == p[-1] and self.isMatch(s[:-1], p[:-1])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
