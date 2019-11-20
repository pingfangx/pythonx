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

        >>> Solution().maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
        6
        """
        # 记录左边
        left = [nums[0]]
        for i in range(1, len(nums)):
            if left[i - 1] > 0:
                left.append(left[i - 1] + nums[i])
            else:
                left.append(nums[i])

        # 记录右边
        right = [nums[-1]]
        for i in range(len(nums) - 1 - 1, -1, -1):
            if right[0] > 0:
                right.insert(0, right[0] + nums[i])
            else:
                right.insert(0, nums[i])

        # 现在记录了左边，也记录了右边，只要左边再加上右边就可以了
        for i in range(len(nums) - 1):
            if right[i + 1] > 0:
                left[i] += right[i + 1]
        return max(left)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
