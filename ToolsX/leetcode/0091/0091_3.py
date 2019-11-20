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

        3
        用 dp 的思想，但是不用数组保存
        https://leetcode.com/problems/decode-ways/discuss/30357/DP-Solution-(Java)-for-reference/29447

        >>> Solution().numDecodings('10')
        1
        >>> Solution().numDecodings('226')
        3
        """
        if not s:
            return 0
        n = len(s)
        pre1 = pre2 = 0 if s[0] == '0' else 1
        for i in range(1, n):
            cur = 0
            if s[i] > '0':  # 可以由前一个数到达当前数，所以值相等
                cur = pre1
            if '10' <= s[i - 1:i + 1] <= '26':  # 可以由前面第二个数到达，所以加上 i-2 的值
                cur += 1 if i < 2 else pre2
            pre1, pre2 = cur, pre1
        return pre1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
