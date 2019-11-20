from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """根据提示，用分治法

        迭代，计算左边部分，右侧连续最大值
        计算 右边部分，左侧连续最大值
        判断并拼接
        超时

        1
        优化一下，计录每个位置的左右连续最大的和
        发现是多余的，其实只需要一个方向就可以了，不需要两个方向再加一次

        2 这次只记录一个方向，同时直接在迭代过程中记录最大值

        >>> Solution().maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
        6
        """
        if not list:
            return 0
        m = nums[0]
        for i in range(1, len(nums)):
            if nums[i - 1] > 0:
                # 左边最大和 > 0 可以累加
                nums[i] += nums[i - 1]
            # 需要在赋值或不赋值后都判断，实际和计算完再求 max 一样了
            if m < nums[i]:
                m = nums[i]
        return m


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
