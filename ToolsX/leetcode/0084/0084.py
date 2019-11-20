from typing import List


class Solution:
    """20190913"""

    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        之前也有过求积水的
        两轮遍历，超时
        >>> Solution().largestRectangleArea([2,1,5,6,2,3])
        10
        """
        if not heights:
            return 0
        n = len(heights)
        max_area = heights[0]
        for i in range(n):  # 从第 i 个开始
            min_height = heights[i]
            max_area = max(max_area, min_height)
            for j in range(i + 1, n):
                min_height = min(min_height, heights[j])
                max_area = max(max_area, min_height * (j - i + 1))
        return max_area


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
