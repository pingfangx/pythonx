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

        4
        https://leetcode.com/problems/decode-ways/discuss/30379/1-liner-O(1)-space
        主要是思路是 reduce 的使用
        以及利用 true 表示 1
        用 乘以 True 或 False 来使得结果为原数或为0

        >>> Solution().numDecodings('10')
        1
        >>> Solution().numDecodings('226')
        3
        """
        # 最后的 [1] 是取出 cur_count
        from functools import reduce
        return reduce(lambda vwp, d: (vwp[1], (d > '0') * vwp[1] + (9 < int(vwp[2] + d) < 27) * vwp[0], d), s,
                      (0, s > '', ''))[1]

    def numDecodings2(self, s):
        # cur_count 赋为 1 或 0
        pre_count, cur_count, pre_num = 0, int(s > ''), ''
        for cur_num in s:
            # pre_count 赋为 cur_count
            # cur_count 和之前的算法一样，加上前一个以及前两个
            # 也就是乘 cur_count 和 pre_count ，可以看到是乘 1 或 0
            pre_count, cur_count, pre_num = cur_count, (cur_num > '0') * cur_count + (
                        9 < int(pre_num + cur_num) < 27) * pre_count, cur_num
        return cur_count


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
