from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """

        在 0121_3 中记录最低、最高，虽然更快，但就无法解决本问题，可以卖出多次
        所以本问题需要用最大子数列解决
        子数列的结束时，累计子数列的值


        12345
        如果是连续增长的，只需要连续子数列就行
        1437
        只要价格降低，就可以卖出，不用担心后面会有更高价，因为卖出后就可以买入当天的低价


        1
        峰谷算法

        2
        答案中的峰谷，注意先找谷，注意 <= 和 >=
        >>> Solution().maxProfit([7,1,5,3,6,4])
        7
        >>> Solution().maxProfit([1,2,3,4,5])
        4
        >>> Solution().maxProfit([7,6,4,3,1])
        0
        """
        total = 0
        i = 1
        while i < len(prices):
            # 找到谷
            while i < len(prices) and prices[i] <= prices[i - 1]:
                i += 1
            valley = prices[i - 1]
            # 找到峰
            while i < len(prices) and prices[i] >= prices[i - 1]:
                i += 1
            peak = prices[i - 1]
            # 累加
            total += peak - valley
        return total


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
