class Solution:
    def mySqrt(self, x: int) -> int:
        """
        从 0 到 n 肯定不行，可以优化为到 n/2

        1
        只计算一次，依然超时，只好用二分的了

        2
        一定要注意验算 0 和 1
        注意 while 和条件的变化
        如果是 low <= high，那么后面 low=mid 要 +1，high=mid 要 -1
        最后退出循环时，high 比 low 小 1，返回 high

        3
        二分

        4
        位运算，从高到低求值
        https://leetcode.com/problems/sqrtx/discuss/25048/Share-my-O(log-n)-Solution-using-bit-manipulation

        5
        应该注意到 16 位可能会溢出
        根据 4 中的优化，从高到低可能会溢出
        先或运算设置值，大于之后再异或取消设置值，可以增加一个变量记录

        >>> Solution().mySqrt(1060472158)
        32564
        """
        answer = 0
        bit = 1 << 15  # 假设是32位 int 最多只需要 16 位
        while bit > 0:
            t = answer | bit
            # if t * t <= x:
            if t <= x / t:
                # 需要设置这一位 1
                answer = t
            bit >>= 1
        return answer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
