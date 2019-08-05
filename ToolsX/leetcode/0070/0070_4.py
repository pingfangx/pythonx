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

        4
        对应答案中的方法5
        wiki 中提示可以用 矩阵快速幂
        [二分幂，快速幂，矩阵快速幂，快速乘](https://blog.csdn.net/MosBest/article/details/69264953)

        >>> Solution().climbStairs(1)
        1
        >>> Solution().climbStairs(2)
        2
        >>> Solution().climbStairs(3)
        3
        >>> Solution().climbStairs(4)
        5
        """
        m = [[1, 1], [1, 0]]
        result = self.matrix_pow(m, n)
        return result[0][0]

    def matrix_pow(self, m, n):
        res = [[1, 0], [0, 1]]
        while n > 0:
            if n & 1 == 1:
                # 如果为奇数,需要乘一次
                res = self.matrix_multiply(res, m)
            m = self.matrix_multiply(m, m)  # 相乘
            n >>= 1  # 除2
        return res

    def matrix_multiply(self, a, b):
        res = []
        for i in range(2):
            res.append([0, 0])
        for i in range(2):
            for j in range(2):
                res[i][j] += a[i][0] * b[0][j] + a[i][1] * b[1][j]
        return res


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
