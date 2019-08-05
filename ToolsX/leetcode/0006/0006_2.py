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

        1
        用指针来移动

       >>> Solution().convert('PAYPALISHIRING',3)
       'PAHNAPLSIIGYIR'
        >>> Solution().convert('PAYPALISHIRING',4)
        'PINALSIGYAHRPI'
        """
        if numRows <= 1:
            return s
        rows = [[] for _ in range(numRows)]
        i = 0
        increase = True
        for c in s:
            rows[i].append(c)
            if increase and i < numRows - 1:
                i += 1
            elif i > 0:
                increase = False
                i -= 1
            else:  # 到达 0
                increase = True
                i += 1

        ans = ''
        for row in rows:
            ans += ''.join(row)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
