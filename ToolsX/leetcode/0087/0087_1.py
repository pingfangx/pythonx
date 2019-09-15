class Solution:
    """20190916"""

    def isScramble(self, s1: str, s2: str) -> bool:
        """
        考二叉树了
        除了叶子节点，都可以交换
        暴力一点，就列出所有的 scrambled string

        1
        https://leetcode.com/problems/scramble-string/discuss/29452/Python-dp-solutions-(with-and-without-memorization).

        >>> Solution().isScramble('abb','bab')
        True
        """
        if len(s1) != len(s2):
            return False
        if s1 == s2:
            return True
        if sorted(s1) != sorted(s2):
            return False
        for i in range(1, len(s1)):
            if (self.isScramble(s1[:i], s2[:i]) and self.isScramble(s1[i:], s2[i:])) or \
                    (self.isScramble(s1[:i], s2[-i:]) and self.isScramble(s1[i:], s2[:-i])):
                return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
