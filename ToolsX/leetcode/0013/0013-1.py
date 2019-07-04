class Solution:
    def romanToInt(self, s: str) -> int:
        """

        由大到小，如果小值后面跟了大值，则要减

        1
        看了讨论，不需要每次都判断，只需要持有 pre 就好了
        >>> Solution().romanToInt('III')
        3
        >>> Solution().romanToInt('IV')
        4
        >>> Solution().romanToInt('IX')
        9
        >>> Solution().romanToInt('LVIII')
        58
        >>> Solution().romanToInt('MCMXCIV')
        1994
        """
        symbols = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        n = 0
        pre = 0
        for c in s:
            cur = symbols[c]
            if pre != 0 and pre < cur:
                # 之前多加的，减掉
                n -= pre
                n -= pre
            pre = cur
            n += cur

        return n


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
