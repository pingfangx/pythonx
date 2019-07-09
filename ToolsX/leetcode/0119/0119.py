from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """

        >>> Solution().getRow(4)
        [1, 4, 6, 4, 1]
        """
        row = [1]
        # 从 0 开始，因为题目要求从 0
        for i in range(0, rowIndex):
            # 错位相加
            row = list(map(lambda x, y: x + y, [0] + row, row + [0]))
        return row


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
