class Solution:
    """20190919"""

    def numDecodings(self, s: str) -> int:
        """
        首先记录各种状态，方便调试
        需要考虑 0 的情况

        1
        会有一些重复的
        >>> Solution().numDecodings('12')
        2
        >>> Solution().numDecodings('226')
        3
        """
        cache = {}
        return self.num_decoding(cache, s)

    def num_decoding(self, cache: dict, s: str) -> int:
        if not s:
            return 1
        else:
            if s[0] == '0':
                return 0
            if len(s) == 1:
                return 1
            if s in cache:
                return cache[s]
            ans = 0
            ans += self.num_decoding(cache, s[1:])  # 截一位
            if len(s) > 1:
                if s[0] == '1' or (s[0] == '2' and s[1] <= '6'):
                    ans += self.num_decoding(cache, s[2:])
            cache[s] = ans
            return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
