class CheckSum:
    """
    检验和
    """

    def __init__(self):
        self.data = []
        """数据，用字符串表示二进制"""

    def add_binary_str(self, x: str):
        n = len(x) // 8
        for i in range(n):
            self.data.append(x[i * 8:(i + 1) * 8])

    def add_int(self, x: int, length: int = 1):
        """

        :param x: 数字
        :param length:补齐字节数
        """
        s = bin(x)[2:]
        s = s.zfill(8 * length)
        self.add_binary_str(s)

    def add_ip(self, x: str):
        """按 . 分割"""
        for s in x.split('.'):
            self.add_int(int(s))

    def check(self, fill_offset=-1):
        """
        :param fill_offset: 填入检验码的位置，如果为 -1 则不填入，而是检验是否正确
        """
        n = len(self.data)

        print(f'计算之前')
        for i in range(0, n - 1, 2):
            line = self.data[i] + self.data[i + 1]
            print(' ' + self.separate_by_length(line))

        ans = self.data[0] + self.data[1]
        print(f'\n第 1 行')
        print(' ' + self.separate_by_length(ans))
        for i in range(2, n - 1, 2):
            line = self.data[i] + self.data[i + 1]
            print(f'\n加上第 {i // 2 + 1} 行')
            print(' ' + self.separate_by_length(ans))
            print('+' + self.separate_by_length(line))
            ans = self.ones_complement_add(ans, line)
            print('=' + self.separate_by_length(ans))
        print(f'按二进制反码求和为\n{self.separate_by_length(ans)}')
        ans = self.ones_complement(ans)

        if fill_offset == -1:
            if eval('0b' + ans) == 0:  # 每一位都是 0，说明求反码前每一位都是 1
                print(f'每一位都是1，检验成功')
            else:
                print(f'检验失败')
            return

        print(f'求反码得到检验和为\n{self.separate_by_length(ans)}')
        print(f'在 {fill_offset} 处填入检验和，重新计算\n')
        n = len(ans) // 8
        for i in range(n):
            self.data[fill_offset + i] = ans[i * 8:(i + 1) * 8]
        self.check(-1)

    @staticmethod
    def ones_complement_add(s1: str, s2: str) -> str:
        """反码求和
        需要 carry，如果最高位产生进位，累加到最低位

        >>> CheckSum().ones_complement_add('00010110','00000011')
        '00011001'
        >>> CheckSum().ones_complement_add('11111111','10000000')
        '10000000'
        """
        if not s1:
            return s2
        if not s2:
            return s1
        n1 = len(s1)
        n2 = len(s2)
        n = max(n1, n2)

        ans = ''
        carry = 0
        for i in range(n):
            c1 = int(s1[n1 - i - 1]) if i < n1 else 0
            c2 = int(s2[n2 - i - 1]) if i < n2 else 0
            t = c1 + c2 + carry  # 相加再加上进位
            if t >= 2:
                t -= 2
                carry = 1
            else:
                carry = 0
            ans = str(t) + ans

        while carry == 1:
            t = ''
            for i in range(n - 1, -1, -1):
                if carry == 1:
                    if ans[i] == '0':  # 直接判断
                        t = '1' + t
                        carry = 0
                    else:
                        t = '0' + t
                        carry = 1
                else:  # 如果没有进位了，原样累加
                    t = ans[i] + t
            ans = t
        return ans

    @staticmethod
    def ones_complement(binary: str):
        """求反码，因为是 str 直接按位反"""
        ans = ''
        for c in binary:
            ans += '1' if c == '0' else '0'
        return ans

    @staticmethod
    def ones_complement_1(binary: str):
        """求反码，不能直接用 ~ ，需要用 mask"""
        if not binary:
            return binary
        n = len(binary)
        b = eval('0b' + binary)
        b = ~b
        mask = (1 << n + 1) - 1  # 生成的 mask 比 b 多一位，且所有位都是 1
        b = b & mask
        return bin(b)[2:][-n:]

    @staticmethod
    def separate_by_length(x: str, length: int = 8):
        """按 8 位输出"""
        n = len(x) // length
        s = ''
        for i in range(n):
            if i > 0:
                s += ' ' * 4
            s += x[i * length:(i + 1) * length]
        return s


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
