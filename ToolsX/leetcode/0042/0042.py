from typing import List


class Solution:
    """20190809"""

    def trap(self, height: List[int]) -> int:
        """
        hard

        穷举来一次

        根据图，想到时的是先一个最高的，然后左右选次高的

        >>> Solution().trap([0,1,0,2,1,0,1,3,2,1,2,1])
        6
        """
        n = len(height)
        if n <= 2:
            return 0
        mid = self.find_highest(height, 0, n - 1)

        ans = 0
        right = mid
        while right >= 2:  # 0 和 1 无法构成
            left = self.find_highest(height, 0, right - 1)
            ans += self.cal_trapped(height, left, right)  # 有了 left right 计算容积
            right = left
        left = mid
        while left <= n - 3:  # n-1 和 n-2 无法构成
            right = self.find_highest(height, left + 1, n - 1)
            ans += self.cal_trapped(height, left, right)  # 计算容积
            left = right
        return ans

    def find_highest(self, height: List[int], start, stop):
        ans = start
        for i in range(start + 1, stop + 1):
            if height[ans] < height[i]:
                ans = i
        return ans

    def cal_trapped(self, height: List[int], start, stop):
        ans = 0
        lower = min(height[start], height[stop])  # 较矮者
        for i in range(start + 1, stop):
            ans += lower - height[i]
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
