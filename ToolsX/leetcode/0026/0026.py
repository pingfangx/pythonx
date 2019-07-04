from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        主要注意删除时下标的变化
        不能继续用下标迭代，因为长度变化了
        """
        if not nums:
            return 0
        pre = nums[0]
        i = 1
        while i < len(nums):
            if nums[i] == pre:
                # 删除
                del nums[i]
                # i 值不处理
                continue
            else:
                # 赋值
                pre = nums[i]
                i += 1
        return len(nums)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
