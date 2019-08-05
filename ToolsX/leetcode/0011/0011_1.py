from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        主要还是读懂题目

        s=w*h
        w=坐标差
        h=最小高
        结果超时了

        1
        超时说明不能双层循环
        仔细看图，当一轮找到最大面积时，往后如果比左边的柱子低，都会被淹没

        还是超时，超时用例为 1-15000
        好难
        >>> Solution().maxArea([1,8,6,2,5,4,8,3,7])
        49
        """
        n = len(height)
        if n <= 1:
            return 0
        max_area = 0
        max_left = 0
        for i in range(n - 1):
            if height[i] <= max_left:
                continue
            for j in range(i + 1, n):
                w = j - i
                h = min(height[i], height[j])
                area = w * h
                if max_area < area:
                    max_area = area
                    max_left = height[i]
        return max_area


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
