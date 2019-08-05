class Solution:
    def intToRoman(self, num: int) -> str:
        """

        1
        https://leetcode.com/problems/integer-to-roman/discuss/6274/Simple-Solution
        这个答案笑到我了
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
        M = ['', 'M', 'MM', 'MMM']
        C = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
        X = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
        I = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
        return M[num // 1000] + C[(num % 1000) // 100] + X[(num % 100) // 10] + I[num % 10]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
