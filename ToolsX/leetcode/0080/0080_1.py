from typing import List


class Solution:
    """20190910"""

    def removeDuplicates(self, nums: List[int]) -> int:
        """前一题是 0026

        1
        还是按 0026 的思路，使用 i 记录正确顺序的 index

        1   1   1
                i
        index-2
        如果相等，说明重复，不需要累加 index

        >>> Solution().removeDuplicates([1,1,1,2,2,3])
        5
        >>> Solution().removeDuplicates([0,0,1,1,1,1,2,3,3])
        7
        """
        n = len(nums)
        if n <= 2:
            return n
        index = 2
        for i in range(2, n):
            if nums[i] > nums[index - 2]:
                nums[index] = nums[i]
                index += 1
        return index


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
