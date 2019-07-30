from collections import Counter, defaultdict
from typing import List


class Solution:
    """20190730"""

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """
        题目很绕，hard 难度，感觉肯定超时
        每个 word 用一遍，可以考虑用 queue

        3
        超时主要是 words 中重复的
        于是思路变成了使用两个 hash map 来保存 word 及其次数

        >>> Solution().findSubstring('barfoothefoobarman',["foo","bar"])
        [0, 9]
        """
        if not s or not words:
            return []
        words_counter = Counter(words)
        word_len = len(words[0])
        words_num = len(words)
        total_len = word_len * words_num
        ans = []
        for i in range(len(s) - total_len + 1):
            seen = defaultdict(int)
            for j in range(i, i + total_len, word_len):
                word = s[j:j + word_len]
                if word in words_counter:
                    seen[word] += 1
                    if seen[word] > words_counter[word]:  # 超限
                        break
                else:  # 不存在，说明不匹配
                    break
            if seen == words_counter:
                ans.append(i)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
