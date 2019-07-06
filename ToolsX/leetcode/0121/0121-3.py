from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        低价买，高价卖
        和之前的思路一样，记录每个位置之前最低的价格，以及每个位置之后最高的价格
        但是这样太慢了

        从前记录最低，从后记录最高，但是这样相遇时不会有结果，比如如果后半部分有更低的价格

        1
        这是一个典型的最大子数列问题，一定要计着了
        但是这样居然是不是快的，原因可能是因为我们用 max 计算了

        2
        手动比较

        3
        看了答案，只记录最小值最大值就可以了，这才是正常的思路，在 0 中好像思路跑偏了
        >>> Solution().maxProfit([7,1,5,3,6,4])
        5
        >>> Solution().maxProfit([7,6,4,3,1])
        0
        """
        if not prices:
            return 0
        min_price = prices[0]
        max_price = 0
        for i in range(1, len(prices)):
            if prices[i] < min_price:
                min_price = prices[i]
            else:
                # 记算差价
                if prices[i] - min_price > max_price:
                    max_price = prices[i] - min_price
        return max_price


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
