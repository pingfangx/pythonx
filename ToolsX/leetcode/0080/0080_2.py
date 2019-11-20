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

        2
        比 1 中的简洁，但是还是觉复 i < 2 的判断像 1 中一样去掉

        >>> Solution().removeDuplicates([1,1,1,2,2,3])
        5
        >>> Solution().removeDuplicates([0,0,1,1,1,1,2,3,3])
        7
        """
        i = 0
        for num in nums:
            if i < 2 or num > nums[i - 2]:
                nums[i] = num
                i += 1
        return i


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
