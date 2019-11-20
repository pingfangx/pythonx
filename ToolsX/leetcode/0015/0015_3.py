from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        遍历是入门，先写一遍

        1
        超时超时

        2
        好像思路不太对，将两个数的和保存在集合中，然后用单个数去比较
        能不能在集合中保存单个数，然后用两个数去比较

        我们回到一开始的两个数和，如果集合中存在 i 的值，说明之前已经有 i 的相反数
        于是从 i 开始，寻找后面是否两个数，其和等于 i 的相反数

        依然超时，应该是判断是否在 ans 中加了一层 O(n)

        3
        原本以为是类似于 two sum
        看了答案结果是双指针
        >>> Solution().threeSum([-1, 0, 1, 2, -1, -4])
        [[-1, 0, 1], [-1, -1, 2]]
        >>> Solution().threeSum([0,0,0])
        [[0, 0, 0]]
        """
        nums.sort()
        n = len(nums)
        answer = []
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left = i + 1
            right = n - 1
            while left < right:
                s = nums[i] + nums[left] + nums[right]
                if s < 0:  # 较小，后移
                    left += 1
                elif s > 0:  # 较大，后移
                    right -= 1
                else:
                    answer.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:  # 过滤相等的值
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1  # 后称、前移
                    right -= 1
        return answer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
