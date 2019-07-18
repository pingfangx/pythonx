class Solution:
    def intToRoman(self, num: int) -> str:
        """
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
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        keys = list(symbols.keys())
        n = len(keys)
        i = n - 1
        ans = ''
        while num > 0:
            value = symbols[keys[i]]
            if num >= value:  # 大于当前值，可以表示
                if i > 0:  # 判断是不是 9
                    pre_value = symbols[keys[i - 1]]
                    if value // pre_value == 5:
                        if num // pre_value == 9:
                            num -= pre_value * 9
                            ans += keys[i - 1]
                            ans += keys[i + 1]
                            i -= 2
                            continue
                if num // value == 4:  # 判断是不是 4
                    num -= value * 4
                    ans += keys[i]
                    ans += keys[i + 1]
                    continue
                num -= value
                ans += keys[i]
            else:
                i -= 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
