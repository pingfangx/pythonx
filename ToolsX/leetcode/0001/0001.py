from typing import List

from leetcode import ListFactory


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        可以双循环，但是 T(n)=O(n^2) 感觉肯定过不了
        想到可以遍历一遍，每个数 - target 但好像没什么用

        >>> Solution().twoSum(ListFactory.create(),-1)
        []
        >>> Solution().twoSum(ListFactory.create(),9)
        [3, 4]
        """
        length = len(nums)
        for i in range(length - 1):
            for j in range(i + 1, length):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
