from typing import List


class Solution:
    """20190825"""

    def getPermutation(self, n: int, k: int) -> str:
        """
        在 0046 中列出了所有排列
        因此思路一，列出所有排列，用索引获取
        思路二，列出排列时计数，到达索引返回
        思路三，n 有 n! 种可能，用可能性直接可知道第几个

        1
        使用索引，虽然肯定还是会超时的

        >>> Solution().getPermutation(3,3)
        '213'
        >>> Solution().getPermutation(4,9)
        '2314'
        """
        ans = []
        self.generate(ans, [], [i + 1 for i in range(n)], k)
        return ans[-1]

    def generate(self, ans: List[str], pre: List[str], nums: List[int], k):
        if len(ans) == k:
            return
        if len(nums) == 0:
            ans.append(''.join(pre))
        else:
            for i, num in enumerate(nums):
                pre.append(str(num))
                nums.pop(i)
                self.generate(ans, pre, nums, k)
                pre.pop()
                nums.insert(i, num)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
