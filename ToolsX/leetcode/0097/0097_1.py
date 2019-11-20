class Solution:
    """20190925"""

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        """
        交错，先来一个暴力美学
        将后者依次插入前者
        插入的过程想到一种思路，只要能找到后者的所有字母，就代表交错

        1
        一开始想判断 s2 是否依次出现于 s3 中，但其实要考虑 s1 s2 交错，于是只比较第一个字母
        还是超时，看来思路不对
        >>> Solution().isInterleave('aabcc','dbbca','aadbbcbcac')
        True
        >>> Solution().isInterleave('aabcc','dbbca','aadbbbaccc')
        False
        """
        if not s1 and not s2 and not s3:  # 都为空
            return True
        if not s3:
            return False
        if not s1 and not s2:  # 两者需要一个不为空
            return False
        c = s3[0]  # s3 不为空，且 s1 不同时为空
        if s1 and s2:
            if s1[0] != c and s2[0] != c:
                return False
        else:  # 至少有一个为空
            if s1 and s1[0] != c:
                return False
            if s2 and s2[0] != c:
                return False
        if s1 and s1[0] == c:
            if self.isInterleave(s1[1:], s2, s3[1:]):
                return True
        if s2 and s2[0] == c:
            if self.isInterleave(s1, s2[1:], s3[1:]):
                return True
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
