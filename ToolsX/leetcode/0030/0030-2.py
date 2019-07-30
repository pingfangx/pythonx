from typing import List


class Solution:
    """20190730"""

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        题目很绕，hard 难度，感觉肯定超时
        每个 word 用一遍，可以考虑用 queue

        1
        改为后移 word 长度，但是有问题，如果 word 是自身重复的，比如 aaa 就不需要后移 word 长度

        2
        加一个方法计算后移的长度
        好不容易处理了各种情况，又超时了，生气

        >>> Solution().findSubstring('aaaccccaab',["cc","cc"])
        [3]
        >>> Solution().findSubstring('wordgoodgoodgoodbestword',["word","good","best","good"])
        [8]
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
        word_n = self.cal_movement(words)
        words_sum_length = len(words[0]) * len(words)
        ans = []
        i = 0
        while i < n - words_sum_length + 1:  # index 可以到 n
            if self.start_with(s[i:], words.copy()):
                ans.append(i)
                # 如何后移
                while True and i < n - words_sum_length:
                    pre = s[i:i + word_n]
                    # 如果后面等于前面，直接添加
                    end = i + words_sum_length
                    suffix = s[end:end + word_n]
                    if pre == suffix:
                        i += word_n
                        ans.append(i)
                    else:
                        break
                i += 1
            else:
                i += 1
        return ans

    def start_with(self, s: str, words: List[str]) -> bool:
        for w in words:
            if s.startswith(w):
                words.remove(w)
                return len(words) == 0 or self.start_with(s[len(w):], words)
        return False

    def cal_movement(self, words: List[str]):
        """计算可后移的长度"""
        first = words[0]
        n = len(first)
        for i in words[1:]:
            if first != i:
                return n
        # 都相等的情况
        return self.cal_min_movement(first)

    def cal_min_movement(self, s: str):
        """
        >>> Solution().cal_min_movement('abcabc')
        3
        >>> Solution().cal_min_movement('ababab')
        2
        >>> Solution().cal_min_movement('aaa')
        1
        >>> Solution().cal_min_movement('abc')
        3
        """
        n = len(s)
        for i in range(1, n // 2 + 1):
            equal = True
            for j in range(n - i - i + 1):
                if s[j:j + i] != s[j + i:j + i + i]:
                    equal = False
                    break
            if equal:  # 找到最小的相等
                return i
        return n


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
