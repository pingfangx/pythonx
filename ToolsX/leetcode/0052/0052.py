from typing import List


class Solution:
    """20190819"""

    def totalNQueens(self, n: int) -> int:
        """
        上一题中给出了解，直接求长度就可以了
        但是可以优化的点在于不需要记录棋盘，只需要记录位置就可以了
        >>> Solution().totalNQueens(4)
        2
        """
        return self.fill_row([], n, 0)

    def fill_row(self, positions: List[tuple], n: int, row: int):
        if row == n:
            return 1
        ans = 0
        for col in range(n):
            available = True
            for position in positions:
                if row == position[0] or col == position[1] or abs(row - position[0]) == abs(col - position[1]):
                    available = False
                    break
            if not available:
                continue
            else:
                positions.append((row, col))
                ans += self.fill_row(positions, n, row + 1)
                positions.pop()
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
