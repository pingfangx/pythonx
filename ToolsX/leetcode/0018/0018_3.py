from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        """
        很喜欢这一系列题啊
        2个用 hashmap
        3个用3个指针
        4个应该在3的基础上再加一个指针，这里先用递归思想解一下，肯定超时，就是觉得很有意思

        1
        排序，去重

        3
        看了答案，好像可以这么解的，只需要优化 twoSum 就行
        >>> Solution().fourSum([5,5,3,5,1,-5,1,-2],4)
        [[-5, 1, 3, 5]]
        >>> Solution().fourSum([1, 0, -1, 0, -2, 2],0)
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
        """
        n = len(nums)
        if n < 4:
            return []
        ans = []
        nums.sort()
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in self.threeSum(nums[i + 1:], target - nums[i]):
                ans.append([nums[i]] + j)
        return ans

    def threeSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        if n < 3:
            return []
        ans = []
        nums.sort()
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in self.twoSum(nums[i + 1:], target - nums[i]):
                ans.append([nums[i]] + j)
        return ans

    def twoSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        if n < 2:
            return []
        ans = []
        nums.sort()
        left = 0
        right = n - 1
        while left < right:
            s = nums[left] + nums[right]
            if s < target:
                left += 1
            elif s > target:
                right -= 1
            else:
                ans.append([nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
