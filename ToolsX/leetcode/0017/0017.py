from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        >>> Solution().letterCombinations('23')
        ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
        """
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
        for num in digits:
            if not ans:
                for c in keyboards[num]:
                    ans.append(c)
            else:
                n = len(ans)
                for i in range(n):
                    for c in keyboards[num]:
                        ans.append(ans[i] + c)  # 每一个元素依次添加一个字母
                # 删除之前的
                ans = ans[n:]
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
