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

        """
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.climbStairs(n - 1) + self.climbStairs(n - 2)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
