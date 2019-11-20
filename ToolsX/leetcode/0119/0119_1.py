from typing import List


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        """

        1
        不使用错位相加，手动实现
        >>> Solution().getRow(4)
        [1, 4, 6, 4, 1]
        """
        row = [1]
        # 从 0 开始，所以 rowIndex+1
        for i in range(1, rowIndex + 1):
            pre = row
            row = [1]
            for j in range(1, i):
                row.append(pre[j - 1] + pre[j])
            row.append(1)
        return row


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
