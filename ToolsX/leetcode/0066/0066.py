from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """

        >>> Solution().plusOne([9])
        [1, 0]
        """
        append = 1
        i = len(digits) - 1
        while i >= 0 and append > 0:
            digits[i] += append
            if digits[i] >= 10:
                digits[i] -= 10
                append = 1
            else:
                append = 0
            i -= 1
        if append == 1:
            digits.insert(0, 1)
        return digits


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
