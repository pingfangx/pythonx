from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        因为是有序的，很容易想到至少应该用二分法
        这里先基本遍历实现一遍，注意不能用 for in range() ，i 只在 range 范围内而不是每次判断
        """
        i = 0
        length = len(nums)
        while i < length:
            if target <= nums[i]:
                return i
            i += 1
        return i


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
