from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """

        1
        0017 中在于先添加，后移除，实际只需要在最后再添加

        2
        空间降不下去，看了答案，不需要字典
        结果还是大
        >>> Solution().letterCombinations('23')
        ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
        """
        if not digits:
            return []
        keyboards = [
            '',
            '',
            'abc',
            'def',
            'ghi',
            'jkl',
            'mno',
            'pqrs',
            'tuv',
            'wxyz',
        ]
        ans = []

        def append(pre, remains):
            if not remains:
                ans.append(pre)
            else:
                number = int(remains[0])
                remains = remains[1:]
                for c in keyboards[number]:
                    append(pre + c, remains)

        append('', digits)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
