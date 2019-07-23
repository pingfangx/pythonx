from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """

        1
        0017 中在于先添加，后移除，实际只需要在最后再添加
        >>> Solution().letterCombinations('23')
        ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
        """
        if not digits:
            return []
        keyboards = {
            '0': '',
            '1': '',
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz',
        }
        ans = []

        def append(pre, remains):
            if not remains:
                ans.append(pre)
            else:
                number = remains[0]
                remains = remains[1:]
                for c in keyboards[number]:
                    append(pre + c, remains)

        append('', digits)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
