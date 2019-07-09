class Solution:
    def addBinary(self, a: str, b: str) -> str:
        """

        1
        优化下
        >>> Solution().addBinary('11','1')
        '100'
        >>> Solution().addBinary('1010','1011')
        '10101'
        """
        append = 0
        buffer = ''
        # a 取为较长者
        if len(a) < len(b):
            a, b = b, a

        # 使用负索引时，边界到达 length
        for i in range(1, len(a) + 1):
            v1 = int(a[-i])
            if i <= len(b):
                v2 = int(b[-i])
            else:
                v2 = 0
            s = v1 + v2 + append
            append, remains = divmod(s, 2)
            buffer = str(remains) + buffer
        if append:
            buffer = '1' + buffer
        return buffer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
