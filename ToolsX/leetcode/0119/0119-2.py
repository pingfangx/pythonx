from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """

        1
        不使用错位相加，手动实现

        2
        错位相加，不使用 map 也可以使用 zip
        >>> Solution().getRow(4)
        [1, 4, 6, 4, 1]
        """
        row = [1]
        for _ in range(rowIndex):
            row = [x + y for x, y in zip(row + [0], [0] + row)]
        return row


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
