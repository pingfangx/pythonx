from typing import List


class Solution:
    """20190730"""

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        题目很绕，hard 难度，感觉肯定超时
        每个 word 用一遍，可以考虑用 queue

        1
        改为后移 word 长度，但是有问题，如果 word 是自身重复的，比如 aaa 就不需要后移 word 长度

        >>> Solution().findSubstring('barfoothefoobarman',["foo","bar"])
        [0, 9]
        >>> Solution().findSubstring('abababab',['ab','ab'])
        [0, 2, 4]
        >>> Solution().findSubstring('aaaaaaaa',['aa','aa','aa'])
        [0, 1, 2]
        """
        if not s or not words:
            return []

        n = len(s)
        word_n = len(words[0])
        ans = []
        i = 0
        while i < n:
            if self.start_with(s[i:], words.copy()):
                ans.append(i)
                # 如何后移
                while True:
                    pre = s[i:i + word_n]
                    # 如果后面等于前面，直接添加
                    end = i + word_n * len(words)
                    suffix = s[end:end + word_n]
                    if pre == suffix:
                        i += word_n
                        ans.append(i)
                    else:
                        i += 1
                        break
            else:
                i += 1
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
