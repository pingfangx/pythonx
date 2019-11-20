class Solution:
    """20190916"""

    def isScramble(self, s1: str, s2: str) -> bool:
        """
        考二叉树了
        除了叶子节点，都可以交换
        暴力一点，就列出所有的 scrambled string
        失败

        >>> Solution().isScramble('abb','bab')
        True
        """
        return len(s1) == len(s2) and s2 in self.scrambled_strings(s1)

    def scrambled_strings(self, s):
        a = set()
        self.scrambled(a, s, 0, len(s))
        return a

    def scrambled(self, a, s, start, end):
        if end - start <= 1:
            a.add(s)
        else:
            mid = start + (end - start) // 2
            self.scrambled(a, s, start, mid)
            self.scrambled(a, s, mid, end)
            s1 = s[:start] + s[mid:end] + s[start:mid] + s[end:]
            if (end - start) & 1 == 1:  # 奇数
                mid += 1
            self.scrambled(a, s1, start, mid)
            self.scrambled(a, s1, mid, end)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
