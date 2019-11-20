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

        2
        看了答案，用两个指针，向中间移动，移动较矮者
        >>> Solution().maxArea([1,8,6,2,5,4,8,3,7])
        49
        """
        if not height:
            return 0
        i = 0
        j = len(height) - 1
        max_area = 0
        while i < j:
            max_area = max(max_area, min(height[i], height[j]) * (j - i))
            if height[i] < height[j]:
                i += 1  # 左边矮，i 右移
            else:
                j -= 1  # 右边矮，j 左移
        return max_area


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
