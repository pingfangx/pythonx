class Solution:
    def climbStairs(self, n: int) -> int:
        """
        感觉可以用递归

        还剩1层    1   1
        还剩2层    2   2,1+1
        还剩3层    3   要么先爬1层，要么先爬2层  爬1层变成2，爬2层变成1
        1，2，1+1

        结果超时了
        再看第4层，3+2
        所以不用递归，直接斐波那契就可以了

        0
        对应答案中方法1
        1
        数列实现
        对应答案中的方法4

        2
        不用判断数列,从 0 和 1 开始加就可以了

        3
        直接用公式行不(可以的答案中的方法6)
        这个公式 a1=1,a2=1 所以少了一项
        题目要求的 n 是际是 a(n+1) 项
        a(n)=sqrt(5)/5*[((1+sqrt(5))/2)**n-((1-sqrt(5))/2)**n]
        a(n+1)=1/sqrt5*[((1+sqrt5)/2)**(n+1)-((1-sqrt5)/2)**(n+1)]

        >>> Solution().climbStairs(1)
        1
        >>> Solution().climbStairs(2)
        2
        >>> Solution().climbStairs(3)
        3
        >>> Solution().climbStairs(4)
        5
        """
        sqrt5 = 5 ** 0.5
        return int(1 / sqrt5 * (((1 + sqrt5) / 2) ** (n + 1) - ((1 - sqrt5) / 2) ** (n + 1)))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
