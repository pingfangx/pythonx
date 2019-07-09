class Solution:
    def romanToInt(self, s: str) -> int:
        """

        由大到小，如果小值后面跟了大值，则要减
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
        length = len(s)
        i = 0
        while i < length:
            c = s[i]

            cur = symbols[c]
            if i + 1 < length:
                nxt = symbols[s[i + 1]]
                if cur < nxt:
                    n += nxt - cur
                    i += 2
                    continue
            n += cur
            i += 1
        return n


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
