from typing import List


class Solution:
    """20190913"""

    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        之前也有过求积水的
        两轮遍历，超时

        1
        https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28917/AC-Python-clean-solution-using-stack-76ms

        >>> Solution().largestRectangleArea([2,1,5,6,2,3])
        10
        """
        heights.append(0)
        stack = [-1]  # 记录升序的 index
        ans = 0
        for i in range(len(heights)):
            while heights[i] < heights[stack[-1]]:  # 当有降序时开始处理
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                ans = max(ans, h * w)
            stack.append(i)
        heights.pop()
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
