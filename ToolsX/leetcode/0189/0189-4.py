from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.

        想一次移动，但要注意
        k 可能大于数组长度，于是求余
        求余可能为 0 ，于是加上判断 k!=len(nums) and len(nums)!=1

        2
        答案中的 3 次翻转的方法

        4
        使用 [:] 优化
        """
        k %= len(nums)
        if k:
            nums[:] = reversed(nums)
            nums[:k] = reversed(list(nums[:k]))
            nums[k:] = reversed(list(nums[k:]))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
