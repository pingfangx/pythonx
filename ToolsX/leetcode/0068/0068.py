from typing import List

from twisted.trial import unittest


class Solution:
    """20190831"""

    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        """
        不喜欢 hard
        """
        ans = []
        n = len(words)

        start = i = 0
        while i < n:
            if self.get_length(words, start, i) <= maxWidth:
                i += 1
                continue
            else:
                ans.append(self.justify(words, start, i - 1, maxWidth))
                start = i
        ans.append(' '.join(words[start:]).ljust(maxWidth))  # 最后一行
        return ans

    def get_length(self, words, start, end) -> int:
        n = 0
        for i in range(start, end + 1):
            n += len(words[i]) + 1
        return n - 1  # 多加了一个空格

    def justify(self, words, start, end, width) -> str:
        """将 justify 理解为，按数量填充空格"""
        extra_space_count = width - self.get_length(words, start, end)
        w = words[start:end + 1]
        n = len(w)
        for i in range(n - 1):  # 计算长度已经包含空格，所以需要添加
            w[i] += ' '
        c = i = 0
        while c < extra_space_count:
            c += 1
            w[i] += ' '
            i += 1
            if i >= n - 1:
                i = 0
        return ''.join(w)


class _Test(unittest.TestCase):
    def test(self):
        _input = ["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain",
                  "to", "a", "computer.", "Art", "is", "everything", "else", "we", "do"]
        _output = Solution().fullJustify(_input, 20)
        _expect = [
            "Science  is  what we",
            "understand      well",
            "enough to explain to",
            "a  computer.  Art is",
            "everything  else  we",
            "do                  "
        ]
        self.assertListEqual(_expect, _output)
