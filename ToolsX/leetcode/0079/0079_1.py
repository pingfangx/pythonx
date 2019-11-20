from typing import List

from twisted.trial import unittest


class Solution:
    """20190909"""

    def exist(self, board: List[List[str]], word: str) -> bool:
        """类似于贪吃蛇

        1
        思路是对的，看了讨论，有可优化的地方
        不需要判断边界，交给方法判断即可
        不需要 pre，置为特殊字符即可
        """
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.find_word(board, word, i, j):
                    return True
        return False

    def find_word(self, board: List[List[str]], word: str, i: int, j: int):
        if word == '':
            return True
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
            return False
        if board[i][j] != word[0]:
            return False
        t = board[i][j]
        board[i][j] = '*'
        w = word[1:]
        ans = self.find_word(board, w, i - 1, j) or self.find_word(board, w, i + 1, j) or self.find_word(
            board, w, i, j - 1) or self.find_word(board, w, i, j + 1)
        board[i][j] = t  # 一定要还原
        return ans


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E']
        ]
        self.assertTrue(Solution().exist(_input, 'ABCCED'))
        self.assertTrue(Solution().exist(_input, 'SEE'))
        self.assertFalse(Solution().exist(_input, 'ABCB'))
