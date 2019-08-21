from typing import List


class Solution:
    """20190821"""

    def canJump(self, nums: List[int]) -> bool:
        """0045-1 中已经解过
        每一步可以走到最远，在走到最远过程中，计算新的最远
        >>> Solution().canJump([0])
        True
        >>> Solution().canJump([2,3,1,1,4])
        True
        >>> Solution().canJump([3,2,1,0,4])
        False
        """
        n = len(nums)
        cur_end = cur_farthest = 0
        for i in range(n):
            cur_farthest = max(cur_farthest, nums[i] + i)
            if i == cur_end:
                if cur_end == cur_farthest:
                    return i == n - 1
                cur_end = cur_farthest
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
