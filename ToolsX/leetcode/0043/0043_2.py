class Solution:
    """20190810"""

    def multiply(self, num1: str, num2: str) -> str:
        """
        大数相乘，不能用内置方法
        可能问题是想问长度较长的整数相加

        1
        实际考查的是乘法公式

            9   8
                7
        =   5   6
        6   3

        2
        优化 index

        0 位 * 0 位，结果为 0 和 1
        1 位 * 0 位，结果为 1 和 2


        >>> Solution().multiply('2','3')
        '6'
        >>> Solution().multiply('123','456')
        '56088'
        """
        n1 = len(num1)
        n2 = len(num2)
        ans = [0] * (n1 + n2)
        for i in range(n1 - 1, -1, -1):
            for j in range(n2 - 1, -1, -1):
                t = int(num1[i]) * int(num2[j])
                t += ans[i + j + 1]  # 累加个位
                ans[i + j + 1] = t % 10  # 个位直接赋值
                ans[i + j] += t // 10  # 十位累加，累加后会在 t+= 时再累加
        ans = [str(i) for i in ans]
        ret = ''.join(ans).lstrip('0')
        if ret == '':
            ret = '0'
        return ret


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
