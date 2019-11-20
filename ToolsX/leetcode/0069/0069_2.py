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

        >>> Solution().mySqrt(1060472158)
        32564
        """
        low = 0
        high = x
        while low <= high:
            mid = low + (high - low) // 2
            if mid ** 2 == x:
                return mid
            elif mid ** 2 < x:
                low = mid + 1
            else:
                high = mid - 1
        return high


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
