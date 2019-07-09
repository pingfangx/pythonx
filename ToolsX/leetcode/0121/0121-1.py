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
        >>> Solution().maxProfit([7,1,5,3,6,4])
        5
        >>> Solution().maxProfit([7,6,4,3,1])
        0
        """
        # 记录 0 因为是收益，可以为 0
        max_ending_here = max_so_far = 0
        for i in range(len(prices) - 1):
            # 如是为负，不会开始记录，如果为正，才记录差值，也就是卖出收益
            # 整个连续子队列记录的就是从记录那天买入，到当前天卖出的收益
            # 而如果 prices[i] - prices[i - 1] > 0 说明前一天卖出的价格不是最高的，于是收益累加上当前比前一天多卖出的
            # 连续子队列继续变长
            max_ending_here = max(0, max_ending_here + prices[i + 1] - prices[i])
            # 连续子队列可能中间中断重新开始，所以记录一个总共的的最大值
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
