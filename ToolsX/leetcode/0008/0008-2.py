class Solution:
    def myAtoi(self, str: str) -> int:
        """
        先自己实现一遍，再使用 python 方法实现一遍

        1
        修改溢出判断

        2
        直接截断，本来想偷懒，结果还是有很多要判断
        >>> Solution().myAtoi('1')
        1
        >>> Solution().myAtoi('   -42')
        -42
        >>> Solution().myAtoi('4193 with words')
        4193
        >>> Solution().myAtoi('words and 987')
        0
        >>> Solution().myAtoi('-91283472332')
        -2147483648
        >>> Solution().myAtoi('-2147483649')
        -2147483648
        >>> Solution().myAtoi('+-2')
        0
        """
        if not str:
            return 0
        str = str.strip()
        if not str:
            return 0

        start = end = -1
        i = 0
        n = len(str)
        while i < n:  # 找出第一个元素位置
            c = str[i]
            if start == -1:
                if c in '+-' or ord('0') <= ord(c) <= ord('9'):
                    start = i
                    i += 1
                    end = i
                else:  # 其他字符退出
                    return 0
            else:  # 有起点了
                if ord('0') <= ord(c) <= ord('9'):  # 数字继续
                    i += 1
                    end = i
                else:  # 结束
                    end = i
                    break
        if end > start:
            try:
                ans = int(str[start:end])
                if ans > ((1 << 31) - 1):  # 溢出判断
                    ans = (1 << 31) - 1
                elif ans < (0 - (1 << 31)):
                    ans = 0 - (1 << 31)
                return ans
            except ValueError:
                pass
        return 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
