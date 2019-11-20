from typing import List


class Sudoku:
    """数独"""

    def __init__(self, board: List[List[str]]):
        self.board = board
        self.possible = [[[str(i) for i in range(1, 10)] for _ in range(9)] for _ in range(9)]
        self.init_possible()

    def solve(self):
        """解数独"""
        while self.judge_possible():
            continue
        if self.success():
            return True
        # 需要猜测
        length, i, j, possibles = self.get_min_possible()
        for num in possibles:
            self.log_d(f'尝试将 {num} 填入 {i},{j},{possibles}')
            t = [[''] * 9 for _ in range(9)]
            self.copy_board(t)
            t[i][j] = num
            sudoku = Sudoku(t)
            if sudoku.solve():  # 得解
                sudoku.copy_board(self.board)  # 复制结果
                return True
            else:
                self.log_d(f'尝试失败')
        return False  # 尝试完依然失败

    def copy_board(self, dst):
        for i, row in enumerate(self.board):
            for j, num in enumerate(row):
                dst[i][j] = self.board[i][j]

    def init_possible(self):
        """更新可能的数字"""
        for i, row in enumerate(self.board):
            for j, num in enumerate(row):
                if num != '.':
                    self.fill(i, j, num)

    def judge_possible(self):
        for i in range(9):
            for j in range(9):
                possibles = self.possible[i][j]
                if len(possibles) == 1:
                    self.fill(i, j, possibles[0])
                    return True

    def get_min_possible(self):
        min_possible = 9, -1, -1, []
        for i in range(9):
            for j in range(9):
                possibles = self.possible[i][j]
                length = len(possibles)
                if length == 2:
                    return length, i, j, possibles
                else:
                    if length < min_possible[0]:
                        min_possible = length, i, j, possibles
        return min_possible

    def success(self) -> bool:
        """是否成功"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '.':
                    return False
        return self.isValidSudoku(self.board)

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """
        解数独让我想起了自己的曾经
        以前用 Python 写代码的时候，是怎么的心理
        现在依然在用 Python 写算法

        只需要依次判断行、列、方格即可

        """
        for i in range(9):
            row = []
            col = []
            grid = []
            grid_row_start, grid_col_start = divmod(i, 3)
            grid_row_start *= 3
            grid_col_start *= 3
            for j in range(9):
                num = board[i][j]  # i 行的每一列
                if num != '.':
                    if num in row:
                        return False
                    else:
                        row.append(num)
                num = board[j][i]  # j 列的每一行
                if num != '.':
                    if num in col:
                        return False
                    else:
                        col.append(num)
                # 012 为第一行,345为第二行
                quotient, remainder = divmod(j, 3)
                num = board[grid_row_start + quotient][grid_col_start + remainder]
                if num != '.':
                    if num in grid:
                        return False
                    else:
                        grid.append(num)
        return True

    @staticmethod
    def log_d(msg):
        # print(msg)
        pass

    def fill(self, i, j, num):
        """填入"""
        self.log_d(f'fill {i},{j},{num}')
        self.board[i][j] = num
        self.possible[i][j].clear()
        for k in range(9):  # 更新行
            self.remove_possible(i, k, num, 'row')  # 第 i 行不可能再有 num
        for k in range(9):  # 更新列
            self.remove_possible(k, j, num, 'col')  # 第 j 列不可能再有 num
        block_i = i // 3 * 3
        block_j = j // 3 * 3
        for i in range(3):  # 更新块
            for j in range(3):
                self.remove_possible(block_i + i, block_j + j, num, 'block')  # 块中不可能再有 num

    def remove_possible(self, i, j, num, pre=''):
        possibles = self.possible[i][j]
        if num in possibles:
            self.log_d(f'{pre} {i}{j}-{num}')
            possibles.remove(num)

    def __str__(self):
        ret = ''
        for i, row in enumerate(self.board):
            if i > 0:
                ret += '\n'
            for j, num in enumerate(row):
                if j > 0:
                    ret += ' '
                    if j % 3 == 0:
                        ret += '\t'
                ret += str(num)
        return ret

    def __repr__(self):
        return self.__str__()


class Solution:
    """20190805"""

    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        0036 中判断了数独，这一题开始解数独了，还是熟悉的配方，只是现在解题，和当初用手机解数独有些不同了
        思路一，不考虑时间复杂度，暴力解
        """
        sudoku = Sudoku(board)
        print(f'解之前\n{sudoku}')
        sudoku.solve()
        print(f'解之后\n{sudoku}')


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
