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

        >>> Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1])
        6
        """
        if not height:
            return 0
        n = len(height)
        left_max = [0] * n
        right_max = [0] * n
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(height[i], left_max[i - 1])
        right_max[-1] = height[-1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(height[i], right_max[i + 1])
        ans = 0
        for i in range(n):
            ans += min(left_max[i], right_max[i]) - height[i]
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
