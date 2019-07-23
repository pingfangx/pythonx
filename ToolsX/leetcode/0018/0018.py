from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        """
        很喜欢这一系列题啊
        2个用 hashmap
        3个用3个指针
        4个应该在3的基础上再加一个指针，这里先用递归思想解一下，肯定超时，就是觉得很有意思
        不排序，可能会有重复的
        >>> Solution().fourSum([1, 0, -1, 0, -2, 2],0)
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
        """
        n = len(nums)
        if n < 4:
            return []
        ans = []
        for i in range(n - 3):
            for j in self.threeSum(nums[i + 1:], target - nums[i]):
                ans.append([nums[i]] + j)
        return ans

    def threeSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        if n < 3:
            return []
        ans = []
        for i in range(n - 2):
            for j in self.twoSum(nums[i + 1:], target - nums[i]):
                ans.append([nums[i]] + j)
        return ans

    def twoSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        if n < 2:
            return []
        ans = []
        for i in range(n - 1):
            for j in nums[i + 1:]:
                if j == target - nums[i]:
                    ans.append([nums[i], j])
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
