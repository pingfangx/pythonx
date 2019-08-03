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
        >>> Solution().searchRange([5,7,7,8,8,10],8)
        [3, 4]
        >>> Solution().searchRange([8,8],8)
        [0, 1]
        >>> Solution().searchRange([1, 2, 2, 3, 4, 4, 4],4)
        [4, 6]
        """
        left, mid, right = self.search(nums, target)
        if mid == -1:
            return [-1, -1]
        start = left
        left = self.search_left(nums[start:mid], target)
        if left == -1:
            left = mid
        else:
            left += start

        start = mid + 1
        right = self.search_right(nums[start:right + 1], target)
        if right == -1:
            right = mid
        else:
            right += start
        return [left, right]

    def search_left(self, nums: List[int], target: int):
        left, mid, right = self.search(nums, target)
        if mid == -1:
            return -1
        else:
            start = left
            left = self.search_left(nums[start: mid], target)  # start:mid 不包含 mid
            if left == -1:
                return mid
            else:
                return left + start

    def search_right(self, nums: List[int], target: int):
        left, mid, right = self.search(nums, target)
        if mid == -1:
            return -1
        else:
            start = mid + 1
            right = self.search_right(nums[start: right + 1], target)
            if right == -1:
                return mid
            else:
                return right + start

    def search(self, nums: List[int], target: int):
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left += 1
            elif nums[mid] > target:
                right -= 1
            else:
                return left, mid, right
        return -1, -1, -1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
