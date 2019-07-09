from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        可以和上一题一样
        但是这样移动次数有点多，但是不这样，del 依然会移动元素
        """
        count = 0
        for i in range(len(nums)):
            if nums[i] != val:
                # 不相等时，先移动元素，再记录，因为是要删除
                nums[count] = nums[i]
                count += 1
        return count


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
