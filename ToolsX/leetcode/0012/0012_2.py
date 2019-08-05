class Solution:
    def intToRoman(self, num: int) -> str:
        """
        2
        看了几个答案，大家把 4 和 9 也挑了出来
        >>> Solution().intToRoman(3)
        'III'
        >>> Solution().intToRoman(4)
        'IV'
        >>> Solution().intToRoman(9)
        'IX'
        >>> Solution().intToRoman(58)
        'LVIII'
        >>> Solution().intToRoman(1994)
        'MCMXCIV'
        """
        if num < 1 or num > 3999:
            return ''

        symbols = {
            'I': 1,
            'IV': 4,
            'V': 5,
            'IX': 9,
            'X': 10,
            'XL': 40,
            'L': 50,
            'XC': 90,
            'C': 100,
            'CD': 400,
            'D': 500,
            'CM': 900,
            'M': 1000
        }
        keys = list(symbols.keys())
        n = len(keys)
        i = n - 1
        ans = ''
        while num > 0:
            value = symbols[keys[i]]
            if num >= value:
                num -= value
                ans += keys[i]
            else:
                i -= 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
