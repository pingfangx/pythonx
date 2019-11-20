from typing import List

from twisted.trial import unittest


class Solution:
    """20190818"""

    def solveNQueens(self, n: int) -> List[List[str]]:
        """
        暴力依次放入
        判断在斜线上可以用 abs(i1-i2)==abs(j1-j2)
        之前在哪本书上看过的，忘了

        1 使用标准解法
        """
        ans = []
        board = [['.'] * n for _ in range(n)]
        self.fill_row(ans, board, n, 0)
        return ans

    def fill_row(self, ans: List[List[str]], board: List[List[str]], n: int, row: int):
        if row == n:
            ans.append([''.join(i) for i in board])
            return
        for col in range(n):
            if not self.is_valid(board, n, row, col):
                continue
            board[row][col] = 'Q'
            self.fill_row(ans, board, n, row + 1)
            board[row][col] = '.'

    def is_valid(self, board, n, row, col):
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        # 135度
        i = row - 1
        j = col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        # 45度
        i = row - 1
        j = col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        # for i in range(row):
        #     for j in range(n):
        #         if board[i][j] == 'Q' and abs(i - row) == abs(j - col):
        #             return False
        return True


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
