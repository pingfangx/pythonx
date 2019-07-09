from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """

        2
        看了讨论，如果 < 9 可以直接返回的
        因为是 +1 所以可以简单处理，不用记录 append
        >>> Solution().plusOne([9])
        [1, 0]
        """
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            else:
                # 肯定是 9 进位继续
                digits[i] = 0
        # 如果退出循环没有 return 则肯定是因为剩余 1
        digits.insert(0, 1)
        return digits


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
