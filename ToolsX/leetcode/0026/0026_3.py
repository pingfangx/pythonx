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

        3
        看了答案记录即可
        """
        if not nums:
            return 0
        count = 0
        for i in range(1, len(nums)):
            if nums[count] != nums[i]:
                count += 1
                nums[count] = nums[i]
        return count + 1


if __name__ == '__main__':
    Solution().removeDuplicates([1, 1, 2])
