from typing import List


class Solution:
    """20190809"""

    def trap(self, height: List[int]) -> int:
        """
        hard

        穷举来一次

        根据图，想到时的是先一个最高的，然后左右选次高的

        1
        计录左右的

        2 答案 4，用左右两个指针

        >>> Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1])
        6
        """
        if not height:
            return 0
        n = len(height)
        left = 0
        right = n - 1
        ans = 0
        left_max = right_max = 0
        while left < right:
            if height[left] < height[right]:  # 左边低，以低为准
                if height[left] >= left_max:
                    left_max = height[left]  # 记录最大值
                else:
                    ans += left_max - height[left]  # 累加结果
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    ans += right_max - height[right]
                right -= 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
