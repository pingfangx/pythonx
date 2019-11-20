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
        n1 = len(s1)
        n2 = len(s2)
        n3 = len(s3)
        if n1 + n2 != n3:
            return False
        dp = [[False] * (n2 + 1) for _ in range(n1 + 1)]
        for i in range(n1 + 1):
            for j in range(n2 + 1):
                if i == 0 and j == 0:
                    dp[i][j] = True
                elif i == 0:
                    dp[i][j] = dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]
                elif j == 0:
                    dp[i][j] = dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]
                else:
                    dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (
                            dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
        return dp[n1][n2]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
