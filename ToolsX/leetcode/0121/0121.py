from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        低价买，高价卖
        和之前的思路一样，记录每个位置之前最低的价格，以及每个位置之后最高的价格
        但是这样太慢了

        从前记录最低，从后记录最高，但是这样相遇时不会有结果，比如如果后半部分有更低的价格
        >>> Solution().maxProfit([7,1,5,3,6,4])
        5
        >>> Solution().maxProfit([7,6,4,3,1])
        0
        """
        if not prices:
            return 0
        low = [prices[0]]
        for i in range(1, len(prices)):
            if prices[i] < low[i - 1]:
                low.append(prices[i])
            else:
                low.append(low[i - 1])
        high = [prices[-1]]
        for i in range(len(prices) - 2, -1, -1):
            if prices[i] > high[0]:
                high.insert(0, prices[i])
            else:
                high.insert(0, high[0])
        # 计算
        return max(0, max([y - x for x, y in zip(low, high)]))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
