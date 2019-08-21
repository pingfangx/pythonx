from typing import List


class Solution:
    """20190821"""

    def canJump(self, nums: List[int]) -> bool:
        """0045-1 中已经解过
        每一步可以走到最远，在走到最远过程中，计算新的最远

        1 答案中的介绍很详细
        >>> Solution().canJump([0])
        True
        >>> Solution().canJump([2,3,1,1,4])
        True
        >>> Solution().canJump([3,2,1,0,4])
        False
        """
        n = len(nums)
        last = n - 1
        for i in range(n - 1, -1, -1):
            if i + nums[i] >= last:
                last = i
        return last == 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
