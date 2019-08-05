from typing import List


class Solution:
    """20190804"""

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """
        解数独让我想起了自己的曾经
        以前用 Python 写代码的时候，是怎么的心理
        现在依然在用 Python 写算法

        只需要依次判断行、列、方格即可

        1
        讨论中的解法也很有意思

        """
        seen = set()
        for i in range(9):
            for j in range(9):
                num = board[i][j]
                if num != '.':
                    in_row = f'{num} in row {i}'
                    if in_row in seen:
                        return False
                    else:
                        seen.add(in_row)

                    in_col = f'{num} in col {j}'
                    if in_col in seen:
                        return False
                    else:
                        seen.add(in_col)

                    in_block = f'{num} in block {i // 3}-{j // 3}'
                    if in_block in seen:
                        return False
                    else:
                        seen.add(in_block)
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
