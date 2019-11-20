from typing import List


class Solution:
    """20190805"""

    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        0036 中判断了数独，这一题开始解数独了，还是熟悉的配方，只是现在解题，和当初用手机解数独有些不同了
        思路一，不考虑时间复杂度，暴力解

        1
        讨论中的解法
        """
        self.print_board(board)
        self.solve(board)
        self.print_board(board)

    def print_board(self, board):
        ret = ''
        for i, row in enumerate(board):
            if i > 0:
                ret += '\n'
            for j, num in enumerate(row):
                if j > 0:
                    ret += ' '
                    if j % 3 == 0:
                        ret += '\t'
                ret += str(num)
        print(ret)

    def solve(self, board: List[List[str]]) -> bool:
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for k in range(1, 10):  # 尝试填入
                        c = str(k)
                        if self.is_valid(board, i, j, c):
                            board[i][j] = c
                            if self.solve(board):
                                return True
                            else:
                                board[i][j] = '.'
                    return False  # 填入 9 个数字都失败
        return True  # 没有 .

    def is_valid(self, board, i, j, c):
        for k in range(9):
            num = board[k][j]  # j 行
            if num != '.' and num == c:
                return False

            num = board[i][k]  # i列
            if num != '.' and num == c:
                return False

            grid_row_start = i // 3 * 3
            grid_col_start = j // 3 * 3
            quotient, remainder = divmod(k, 3)
            num = board[grid_row_start + quotient][grid_col_start + remainder]
            if num != '.' and num == c:
                return False
        return True


if __name__ == '__main__':
    Solution().solveSudoku(
        board=[
            [".", ".", "9", "7", "4", "8", ".", ".", "."],
            ["7", ".", ".", "6", ".", "2", ".", ".", "."],
            [".", "2", ".", "1", ".", "9", ".", ".", "."],
            [".", ".", "7", "9", "8", "6", "2", "4", "1"],
            ["2", "6", "4", "3", "1", "7", "5", "9", "8"],
            ["1", "9", "8", "5", "2", "4", "3", "6", "7"],
            [".", ".", ".", "8", "6", "3", ".", "2", "."],
            [".", ".", ".", "4", "9", "1", ".", ".", "6"],
            [".", ".", ".", "2", "7", "5", "9", ".", "."]
        ])
