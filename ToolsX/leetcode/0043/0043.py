class Solution:
    """20190810"""

    def multiply(self, num1: str, num2: str) -> str:
        """
        大数相乘，不能用内置方法
        可能问题是想问长度较长的整数相加

        >>> Solution().multiply('2','3')
        '6'
        >>> Solution().multiply('123','456')
        '56088'
        """
        if num1 == '0' or num2 == '0':
            return '0'
        n1 = len(num1)
        n2 = len(num2)
        if n1 > n2:
            n1, n2 = n2, n1
            num1, num2 = num2, num1
        ans = ''
        while num1 != '':
            # 除了减1，可以优化为二分相乘
            num1 = self.str_sub1(num1)
            ans = self.str_add(ans, num2)
        return ans

    def str_add(self, num1: str, num2: str) -> str:
        """
        >>> Solution().str_add('123','456')
        '579'
        >>> Solution().str_add('123','4567')
        '4690'
        """
        n1 = len(num1)
        n2 = len(num2)
        if n1 > n2:
            n1, n2 = n2, n1
            num1, num2 = num2, num1
        # n1 较小
        ans = []
        carry = 0
        for i in range(1, n2 + 1):
            if i <= n1:
                t = int(num1[-i]) + int(num2[-i]) + carry
            else:
                t = int(num2[-i]) + carry
            if t >= 10:
                t -= 10
                carry = 1
            else:
                carry = 0
            ans.insert(0, str(t))
        if carry == 1:
            ans.insert(0, '1')
        return ''.join(ans).lstrip('0')

    def str_sub1(self, num: str) -> str:
        """
        >>> Solution().str_sub1('2100')
        '2099'
        """
        ans = []
        n = len(num)
        carry = 1
        for i in range(n - 1, -1, -1):
            t = int(num[i])
            if t < carry:
                t += 10
                t -= carry
                carry = 1
                ans.insert(0, str(t))
            else:
                t -= carry
                carry = 0
                ans.insert(0, str(t))
        return ''.join(ans).lstrip('0')


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
