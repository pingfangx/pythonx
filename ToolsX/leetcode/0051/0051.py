from typing import List

from twisted.trial import unittest


class Solution:
    """20190818"""

    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        暴力依次放入
        判断在斜线上可以用 abs(i1-i2)==abs(j1-j2)
        之前在哪本书上看过的，忘了
        """
        ans = []
        board = [['.'] * n for _ in range(n)]
        self.fill_row(ans, board, [], n, 0)
        return ans

    def fill_row(self, ans: List[List[str]], board: List[List[str]], positions: List[tuple], n: int, row: int):
        """填入行"""
        if row == n:
            ans.append([''.join(i) for i in board])
            return
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
                board[row][col] = 'Q'
                self.fill_row(ans, board, positions, n, row + 1)
                positions.pop()
                board[row][col] = '.'


class _Test(unittest.TestCase):
    def test(self):
        _input = 4
        _output = Solution().solveNQueens(_input)
        _expect = [
            [".Q..",
             "...Q",
             "Q...",
             "..Q."],

            ["..Q.",
             "Q...",
             "...Q",
             ".Q.."]
        ]
        self.assertListEqual(_expect, _output)
