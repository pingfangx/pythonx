from typing import List


class Solution:
    """20190910"""

    def removeDuplicates(self, nums: List[int]) -> int:
        """前一题是 0026

        >>> Solution().removeDuplicates([1,1,1,2,2,3])
        5
        >>> Solution().removeDuplicates([0,0,1,1,1,1,2,3,3])
        7
        """
        n = len(nums)
        duplicate = 0
        for i in range(2, n):
            if nums[i] == nums[i - duplicate - 2]:
                duplicate += 1
            nums[i - duplicate] = nums[i]  # 向前移
        return n - duplicate


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
