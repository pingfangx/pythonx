from typing import List


class Solution:
    """20190808"""

    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        0808 是不是奥运会，感觉好久了呀
        连差好几个 hard 难度，hard 是有点头疼啊

        要求 T(n)=O(n),S(n)=O(1)
        如果排序，则一般都是 O(n log n)，所以要在一轮遍历中找出

        我在想，如果用 hash map 一轮保存数据求 max，二轮从 map 中取出判断，算不算是 O(2n)

        错误，因为第二轮循环不是 O(n) 而是 O(m)


        1

        

        >>> Solution().firstMissingPositive([3,4,-1,1])
        2
        >>> Solution().firstMissingPositive([7,8,9,11,12])
        1
        """
        n = len(nums)
        for i in range(n):
            while 0 < nums[i] <= n and nums[nums[i] - 1] != nums[i]:  # 将 nums[i] 的值放在对应的 index
                t = nums[i]
                nums[i] = nums[nums[i] - 1]
                nums[t - 1] = t  # 注意 nums[i] 已经变化，要用 t-1
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
