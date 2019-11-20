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


        >>> Solution().multiply('2','3')
        '6'
        >>> Solution().multiply('123','456')
        '56088'
        """
        n1 = len(num1)
        n2 = len(num2)
        ans = [0] * (n1 + n2)
        for i in range(n1):
            for j in range(n2):
                t = int(num2[n2 - 1 - j]) * int(num1[n1 - 1 - i])
                k = n1 + n2 - 1 - i - j
                ans[k] += t % 10
                ans[k - 1] += t // 10
        carry = 0
        for i in range(n1 + n2 - 1, -1, -1):
            ans[i] += carry
            carry = 0
            while ans[i] >= 10:
                ans[i] -= 10
                carry += 1
        ans = [str(i) for i in ans]
        ret = ''.join(ans).lstrip('0')
        if ret == '':
            ret = '0'
        return ret


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
