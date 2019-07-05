from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """根据提示，用分治法

        迭代，计算左边部分，右侧连续最大值
        计算 右边部分，左侧连续最大值
        判断并拼接
        超时


        >>> Solution().maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
        6
        """
        # 不正确，这种方式好把所有正数累加了，其实要求的是连续的
        # if len(nums) == 1:
        #     return nums[0]
        # else:
        #     mid = len(nums) // 2
        #     left = self.maxSubArray(nums[:mid])
        #     right = self.maxSubArray(nums[mid:])
        #     if left > 0 or right > 0:
        #         if left > 0 and right > 0:
        #             return left + right
        #         elif left > 0:
        #             return left
        #         else:
        #             return right
        #     else:
        #         return left if left > right else right
        m = None
        for i in range(len(nums)):
            left = self.max_right(nums[:i])
            right = self.max_left(nums[i + 1:])
            s = nums[i]
            if left > 0:
                s += left
            if right > 0:
                s += right
            if m is None or m < s:
                m = s
        return m

    def max_right(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        left = self.max_right(nums[:-1])
        if left > 0:
            return left + nums[-1]
        else:
            return nums[-1]

    def max_left(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        right = self.max_left(nums[1:])
        if right > 0:
            return right + nums[0]
        else:
            return nums[0]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
