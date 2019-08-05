from typing import List


class Solution:
    """20190730"""

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        题目很绕，hard 难度，感觉肯定超时
        每个 word 用一遍，可以考虑用 queue

        >>> Solution().findSubstring('barfoothefoobarman',["foo","bar"])
        [0, 9]
        """
        if not s or not words:
            return []

        n = len(s)
        ans = []
        for i in range(n):
            if self.start_with(s[i:], words.copy()):
                ans.append(i)
        return ans

    def start_with(self, s: str, words: List[str]) -> bool:
        for w in words:
            if s.startswith(w):
                words.remove(w)
                return len(words) == 0 or self.start_with(s[len(w):], words)
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
