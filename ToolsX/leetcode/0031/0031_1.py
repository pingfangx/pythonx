from typing import List


class Solution:
    """20190731"""

    def nextPermutation(self, nums: List[int]) -> None:
        """
        有一个只考虑结果，不考虑复杂度的暴力实现，按顺序列出所有可能

        1
        可以考虑从后向前查找数字变小的，然后交换，但是好像有特殊情况
        看了答案，思路是对的，就是自己解不出来，因为仅交换还不行

        从右向左，查找减小的数字
        找出比减小的数大的数字，交换
        排序剩余部分

        >>> a=[0,0,4,2,1,0]
        >>> Solution().nextPermutation(a)
        >>> a
        [0, 1, 0, 0, 2, 4]

        """
        index = -1
        n = len(nums)
        for i in range(n - 1, 0, -1):  # 1 查找减小的
            if nums[i - 1] < nums[i]:
                index = i - 1
                break
        if index == -1:
            nums.sort()
            return
        # 查找比 index 大的
        j = n - 1  # 默认取最后一个
        for i in range(index, n - 1):
            if nums[i + 1] <= nums[index]:
                j = i
                break
        nums[index], nums[j] = nums[j], nums[index]  # 2 交换
        # 排序
        t = nums[index + 1:]
        t.sort()
        while len(nums) > index + 1:
            nums.pop()
        nums.extend(t)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
