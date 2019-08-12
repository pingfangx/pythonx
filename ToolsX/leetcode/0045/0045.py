from typing import List


class Solution:
    """20190812"""

    def jump(self, nums: List[int]) -> int:
        """
        很有意思的题
        需要注意的是，如果倒数第3个是 1 那肯定不能跳 2 到终点
        如果是 2 ，那就不用跳到倒数第2个，直接到终点
        [1,1,1]
        [2,1,1]
        超时，应该考虑可以一遍到达终点
        >>> Solution().jump([2,3,1,1,4])
        2
        """
        n = len(nums)
        if n <= 1:
            return 0
        for i in range(n):
            if nums[i] >= n - 1 - i:  # 可以直接到终点
                return 1 + self.jump(nums[:i + 1])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
