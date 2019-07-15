class Solution:
    def convert(self, s: str, numRows: int) -> str:
        """
        一开始以为是排成 H 型的
        A       E
        B   D   F
        C       G
        想到可以4个一组，求余分配
        后来发现有参数 numRows，不过也一样，可以分组
        A           G
        B       F
        C   E
        D
        >>> Solution().convert('PAYPALISHIRING',3)
        'PAHNAPLSIIGYIR'
        >>> Solution().convert('PAYPALISHIRING',4)
        'PINALSIGYAHRPI'
        """
        group_count = numRows * 2 - 2
        if group_count <= 1:
            return s
        n = len(s)
        rows = [[] for _ in range(numRows)]
        for i in range(n):
            remainder = i % group_count
            if remainder >= numRows:
                # 4 5 对应 2 1
                # remainder = numRows = 1 - (remainder - numRows + 1)
                remainder = numRows * 2 - remainder - 2
            rows[remainder].append(s[i])
        ans = ''
        for row in rows:
            ans += ''.join(row)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
