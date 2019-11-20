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

        >>> Solution().getPermutation(3,2)
        '132'
        >>> Solution().getPermutation(3,3)
        '213'
        >>> Solution().getPermutation(4,9)
        '2314'
        """
        ans = ''
        nums = [i + 1 for i in range(n)]

        product = {1: 1}  # 计算 [1,n-1] 各数阶乘
        for i in range(2, n):
            product[i] = i * product[i - 1]

        while len(nums) > 1 and k > 1:  # 当 k==1 时说明只有一种情况，直接拼接就可以了
            p = product[len(nums) - 1]
            index = k // p  # 0 倍表示取第一个数，1 倍表示第二轮，取第二个数
            if index == k / p:  # 恰好整除， index 需要 -1
                index -= 1
            ans += str(nums[index])
            nums.pop(index)
            k -= index * p
        for num in nums:
            ans += str(num)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
