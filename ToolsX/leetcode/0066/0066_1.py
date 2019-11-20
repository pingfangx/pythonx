from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """

        1
        尝试一行
        原始  [1,9]
        转为 str 数组   ['1','9']
        join    '19'
        转为 int  19
        +1  20
        转为 str  '20'
        转为数组    [2,0]

        >>> Solution().plusOne([9])
        [1, 0]
        """
        return [int(c) for c in str(int(''.join([str(i) for i in digits])) + 1)]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
