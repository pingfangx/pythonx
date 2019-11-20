from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        可以和上一题一样
        但是这样移动次数有点多，但是不这样，del 依然会移动元素

        1
        答案中方法 2
        每当有相等的，就从最后取一个元素放到当前位置，同时减小长度
        """
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                # 赋值最后一个元素
                nums[i] = nums[n - 1]
                n -= 1
                # i 没 -1 继续判断
            else:
                i += 1
        return n


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
