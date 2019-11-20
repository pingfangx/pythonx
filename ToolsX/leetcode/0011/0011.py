from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        主要还是读懂题目

        s=w*h
        w=坐标差
        h=最小高
        结果超时了
        >>> Solution().maxArea([1,8,6,2,5,4,8,3,7])
        49
        """
        n = len(height)
        if n <= 1:
            return 0
        max_area = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                w = j - i
                h = min(height[j], height[i])
                max_area = max(max_area, w * h)
        return max_area


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
