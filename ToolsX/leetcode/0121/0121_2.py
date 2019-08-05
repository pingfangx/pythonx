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
        >>> Solution().maxProfit([7,1,5,3,6,4])
        5
        >>> Solution().maxProfit([7,6,4,3,1])
        0
        """
        # 记录 0 因为是收益，可以为 0
        max_ending_here = max_so_far = 0
        for i in range(len(prices) - 1):
            max_ending_here += prices[i + 1] - prices[i]
            if max_ending_here > 0:
                # 如果大于 0 ，说明起始那天依然是最低价，子数列继续，并且总计的最大值也会累计
                if max_so_far < max_ending_here:
                    max_so_far = max_ending_here
            else:
                # 否则，说明价格降低，也就是当天价格比前面的最低价还要低，子数列结束
                # 如果当天之后价格，就会形成新的子数列
                max_ending_here = 0
        return max_so_far


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
