from typing import List


class Solution:
    """20190804"""

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

    def test(self):
        """
        >>> Solution().test()
        False
        """
        board = [
            ["8", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"]
        ]
        return self.isValidSudoku(board)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
