from typing import List


class Solution:
    """20190803"""

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        要求 O(log n)

        向左边查找，再向右边查找，要执行 2 log n 次，优化一下

        1
        0034 中多搜索了第一步，优化一下
        还是一样的慢

        2 答案中的方法，不太理解

        >>> Solution().searchRange([5,7,7,8,8,10],8)
        [3, 4]
        >>> Solution().searchRange([8,8],8)
        [0, 1]
        >>> Solution().searchRange([1, 2, 2, 3, 4, 4, 4],4)
        [4, 6]
        """
        ans = [-1, -1]
        left = self.search(nums, target, True)
        if left == len(nums) or nums[left] != target:
            return ans
        ans[0] = left
        ans[1] = self.search(nums, target, False) - 1
        return ans

    def search(self, nums: List[int], target: int, find_left: bool) -> int:
        left = 0
        right = len(nums)
        while left < right:  # left==right 才退出
            mid = left + (right - left) // 2
            if nums[mid] > target or (find_left and nums[mid] == target):
                right = mid
            else:
                left = mid + 1
        return left


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
