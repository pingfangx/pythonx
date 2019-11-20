class Solution:
    """20190919"""

    def numDecodings(self, s: str) -> int:
        """
        首先记录各种状态，方便调试
        需要考虑 0 的情况

        1
        会有一些重复的

        2
        https://leetcode.com/problems/decode-ways/discuss/30358/Java-clean-DP-solution-with-explanation/207715
        练习 dp
        >>> Solution().numDecodings('12')
        2
        >>> Solution().numDecodings('226')
        3
        """
        if not s:
            return 0
        n = len(s)
        dp = [0] * n
        if s[0] != '0':
            dp[0] = 1
        for i in range(1, n):
            if s[i] > '0':  # 可以由前一个数到达当前数，所以值相等
                dp[i] = dp[i - 1]
            if s[i - 1] == '1' or (s[i - 1] == '2' and s[i] <= '6'):  # 可以由前面第二个数到达，所以加上 i-2 的值
                dp[i] += 1 if i < 2 else dp[i - 2]
        return dp[n - 1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
