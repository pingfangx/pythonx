class Solution:
    """20190817"""

    def myPow(self, x: float, n: int) -> float:
        """
        在之前的爬楼梯问题计论了斐波那契问题
        斐波那契介绍了矩阵幂
        矩阵幂介绍了二分幂和二进制幂
        因为这里 x 是 float 所以用二分幂的思想处理

        示例
        x^10                    ans=1   t=x             n=10
        x^(5*2)                 幂的乘方，指数相乘
        (x^5)^2                 ans=1   t=x^2           n=5
        (x^(4+1))^2             同底数幂相乘，指数相加
        (x^4*x^1)^2             积的乘方=乘方的积
        (x^4)^2 * (x^1)^2       ans=x^2 t=(x^2)^2       n=2
        ((x^2)^2)^2 * (x^1)^2   ans=x^2 t=((x^2)^2)^2   n=1
        ans=(x^2)*((x^2)^2)^2           t=              n=0

        >>> Solution().myPow(2.1,3)
        9.261
        >>> Solution().myPow(2,-2)
        0.25
        """
        negative = False
        if n < 0:
            negative = True
            n = -n
        ans = 1
        while n:
            if n & 1 == 1:  # 奇数
                ans *= x  # 奇数或最后为 1 乘到 ans 上
            x *= x
            n >>= 1
        return ans if not negative else 1 / ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
