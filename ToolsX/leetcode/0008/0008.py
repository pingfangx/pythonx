class Solution:
    def myAtoi(self, str: str) -> int:
        """
        先自己实现一遍，再使用 python 方法实现一遍
        >>> Solution().myAtoi('   -42')
        -42
        >>> Solution().myAtoi('4193 with words')
        4193
        >>> Solution().myAtoi('words and 987')
        0
        >>> Solution().myAtoi('-91283472332')
        -2147483648
        """
        if not str:
            return 0

        i = 0
        n = len(str)
        signum = 1
        while i < n:  # 找出第一个元素位置
            c = str[i]
            if c == ' ':  # 空格继续，可以直接 trim
                i += 1
            elif c == '-':
                signum = -1
                i += 1  # 后移到元素位
                break
            elif c == '+':
                signum = 1
                i += 1
                break
            elif ord('0') <= ord(c) <= ord('9'):
                break
            else:  # 其他字符退出
                break
        ans = 0
        while i < n:  # 求值
            c = str[i]
            if ord('0') <= ord(c) <= ord('9'):
                # num = int(c)
                num = ord(c) - ord('0')  # 比 int() 还快？
                ans *= 10
                ans += num
            else:  # 非数字字符
                break
            i += 1
        ans = ans * signum  # 符号
        if ans > ((1 << 31) - 1):  # 溢出判断
            ans = (1 << 31) - 1
        elif ans < (0 - (1 << 31)):
            ans = 0 - (1 << 31)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
