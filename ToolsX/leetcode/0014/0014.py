from typing import List


class Solution:

    def longestCommonPrefix(self, strs: List[str]) -> str:
        """
        按顺序比较就好了

        T(n)=O(s)
        s 是所有字符串总长度，如果有 n 个 均为 m 长的字符串
        最坏需要 n*m 次比较
        最好需要 n*minLen 次
        """
        if not strs:
            return ''
        first = strs[0]
        if len(strs) == 1:
            return first

        buffer = ''
        for i in range(len(first)):
            c = first[i]
            for str in strs[1:]:
                if i >= len(str) or str[i] != c:
                    return buffer
            # 所有的字符中都有 c 添加
            buffer += c
        return buffer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
