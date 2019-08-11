class Solution:
    """20190811"""

    def isMatch(self, s: str, p: str) -> bool:
        """
        匹配 ? 和 *
        又是各种判断

        1
        看讨论，还是思路不对，不应该从后向前的
        https://leetcode.com/problems/wildcard-matching/discuss/17810/Linear-runtime-and-constant-space-solution

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
        si = pi = 0
        ts = 0
        tp = -1
        sn = len(s)
        pn = len(p)
        while si < sn:
            if pi < pn and (p[pi] == '?' or p[pi] == s[si]):  # 两个都前进
                si += 1
                pi += 1
            elif pi < pn and p[pi] == '*':
                tp = pi
                ts = si
                pi += 1
            elif tp != -1:
                pi = tp + 1
                ts += 1
                si = ts
            else:
                return False
        while pi < pn and p[pi] == '*':
            pi += 1
        return pi == pn


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
