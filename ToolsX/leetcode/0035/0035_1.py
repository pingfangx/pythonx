from typing import List

from leetcode import ListFactory


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        因为是有序的，很容易想到至少应该用二分法
        这里先基本遍历实现一遍，注意不能用 for in range() ，i 只在 range 范围内而不是每次判断


        查找出一个 < target 的位置

        怎么一直理不清楚，太笨了，画图
        1   2   3   4   找 3
        l       m   h   继续向前找
        l   m   h       m < target 再看看 m 后还有没有

        >>> Solution().searchInsert(ListFactory.from_num(123),0)
        0
        >>> Solution().searchInsert(ListFactory.from_num(123),3)
        2
        >>> Solution().searchInsert(ListFactory.from_num(123),4)
        3
        """
        low = 0
        high = len(nums) - 1
        mid = (low + high) // 2
        while low < mid:
            if nums[mid] < target:
                # 如果中间数 < target 继续向后找，看还有没有比 target 小的
                low = mid
            else:
                # 如果中间数 >= target，继续向前找
                high = mid
            mid = (low + high) // 2
        # 退出循环时的状态，low=high 或 low+1=high，但是不能确定 low 和 high 处与 target 的关系
        if nums[high] < target:
            return high + 1
        else:
            if nums[low] < target:
                return low + 1
            else:
                return low


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
