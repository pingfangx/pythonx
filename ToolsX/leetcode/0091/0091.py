from typing import List


class Solution:
    """20190919"""

    def numDecodings(self, s: str) -> int:
        """
        首先记录各种状态，方便调试
        需要考虑 0 的情况
        >>> Solution().numDecodings('12')
        2
        >>> Solution().numDecodings('226')
        3
        """
        ans = []
        self.num_decoding(ans, [], s)
        return len(ans)

    def num_decoding(self, ans: List[List[str]], pre: List[str], s: str):
        if not s:
            ans.append(pre.copy())
        else:
            if s[0] == '0':  # 认为划分不正确，不进行后续处理
                return
            # 取一位
            self.num_decoding(ans, pre + [s[0]], s[1:])
            # 取二位
            if len(s) > 1:
                if s[0] == '1' or (s[0] == '2' and s[1] <= '6'):
                    self.num_decoding(ans, pre + [s[0:2]], s[2:])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
