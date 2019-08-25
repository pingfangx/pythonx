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

        2
        选出第一个数字，剩余 n-1 个，有 (n-1)! 种可能
        用 k/(n-1)! 得到的倍数即为第几轮
        如 123 以 1 开头有 2 种可能
        213 有 2 种可能
        如果 k 为 3 ，3//2==1 说明是第二轮

        3
        https://leetcode.com/problems/permutation-sequence/discuss/22512/Share-my-Python-solution-with-detailed-explanation

        >>> Solution().getPermutation(3,3)
        '213'
        >>> Solution().getPermutation(3,3)
        '213'
        >>> Solution().getPermutation(4,9)
        '2314'
        """
        import math
        ans = ''
        nums = list(range(1, n + 1))
        k -= 1  # 需要 -1
        while n > 0:
            n -= 1
            index, k = divmod(k, math.factorial(n))
            ans += str(nums[index])
            nums.pop(index)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
