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

        3 记录最大值即可
        如何理解，想求当前位置加上左侧的最大和，只需求出左边的和，如果 > 0　就加上，否则当前值就是最大和

        >>> Solution().maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
        6
        """
        if not list:
            return 0
        cur_sum = max_sum = nums[0]
        for num in nums[1:]:
            if cur_sum < 0:
                cur_sum = num
            else:
                cur_sum += num
            if max_sum < cur_sum:
                max_sum = cur_sum
        return max_sum


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
