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

        >>> Solution().mySqrt(1060472158)
        32564
        """
        answer = 0
        bit = 1 << 15  # 假设是32位 int 所以从 16 位开始
        while bit > 0:
            answer |= bit  # 将这一位设为 1
            if answer * answer > x:  # 说明加上这一位的 1 就大了，说明不能加，恢复
                answer ^= bit  # bit 只有最高位为 1，异或将 answer 这一位置为 0
            bit >>= 1
        return answer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
