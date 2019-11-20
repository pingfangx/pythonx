from typing import List

from twisted.trial import unittest


class Solution:
    """20190909"""

    def exist(self, board: List[List[str]], word: str) -> bool:
        """类似于贪吃蛇"""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.find_word([], board, word, i, j):
                    return True
        return False

    def find_word(self, pre: List, board: List[List[str]], word: str, i: int, j: int):
        if board[i][j] != word[0]:
            return False
        if len(word) == 1:
            return True
        pre.append((i, j))  # 记录当前位置
        if i > 0 and (i - 1, j) not in pre:  # 上移
            if self.find_word(pre, board, word[1:], i - 1, j):
                return True
        if i < len(board) - 1 and (i + 1, j) not in pre:  # 下移
            if self.find_word(pre, board, word[1:], i + 1, j):
                return True
        if j > 0 and (i, j - 1) not in pre:  # 左移
            if self.find_word(pre, board, word[1:], i, j - 1):
                return True
        if j < len(board[0]) - 1 and (i, j + 1) not in pre:  # 右移
            if self.find_word(pre, board, word[1:], i, j + 1):
                return True
        pre.remove((i, j))  # 不可用，移除
        return False


class _Test(unittest.TestCase):
    def test(self):
        _input = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E']
        ]
        self.assertTrue(Solution().exist(_input, 'SEE'))
        self.assertTrue(Solution().exist(_input, 'ABCCED'))
        self.assertFalse(Solution().exist(_input, 'ABCB'))
