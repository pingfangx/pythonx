class Solution:
    """20190924"""

    def numTrees(self, n: int) -> int:
        """
        前一题是列出所有可能
        讨论中还有种种解法，可以参考

        https://leetcode.com/problems/unique-binary-search-trees/discuss/31706/Dp-problem.-10%2B-lines-with-comments

        Taking 1~n as root respectively:
           1 as root: # of trees = F(0) * F(n-1)  // F(0) == 1
           2 as root: # of trees = F(1) * F(n-2)
           3 as root: # of trees = F(2) * F(n-3)
           ...
           n-1 as root: # of trees = F(n-2) * F(1)
           n as root:   # of trees = F(n-1) * F(0)

        So, the formulation is:
           F(n) = F(0) * F(n-1) + F(1) * F(n-2) + F(2) * F(n-3) + ... + F(n-2) * F(1) + F(n-1) * F(0)
        >>> Solution().numTrees(3)
        5
        """
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1
        for i in range(2, n + 1):
            for j in range(1, i + 1):
                dp[i] += dp[j - 1] * dp[i - j]
        return dp[n]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
