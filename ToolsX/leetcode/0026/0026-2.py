from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        主要注意删除时下标的变化
        不能继续用下标迭代，因为长度变化了

        1
        不需要 每次调用 len 自己记录

        2
        不需要 pre
        """
        length = len(nums)
        i = 1
        while i < length:
            if nums[i] == nums[i - 1]:
                # 删除
                del nums[i]
                length -= 1
            else:
                i += 1
        return length


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
