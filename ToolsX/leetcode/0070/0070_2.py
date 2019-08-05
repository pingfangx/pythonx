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
        """
        s1 = 0
        s2 = 1
        for i in range(n):
            s1, s2 = s2, s1 + s2
        return s2


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
