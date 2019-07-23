from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        """
        很喜欢这一系列题啊
        2个用 hashmap
        3个用3个指针
        4个应该在3的基础上再加一个指针，这里先用递归思想解一下，肯定超时，就是觉得很有意思

        1
        排序，去重

        2
        正式求解，尝试使用 4 个指针
        >>> Solution().fourSum([5,5,3,5,1,-5,1,-2],4)
        [[-5, 1, 3, 5]]
        >>> Solution().fourSum([1, 0, -1, 0, -2, 2],0)
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
        """
        n = len(nums)
        if n < 4:
            return []
        ans = []
        nums.sort()
        for n1 in range(n - 3):
            if n1 > 0 and nums[n1] == nums[n1 - 1]:
                continue
            for n2 in range(n1 + 1, n - 2):
                if n2 > n1 + 1 and nums[n2] == nums[n2 - 1]:
                    continue
                n3 = n2 + 1
                n4 = n - 1
                while n3 < n4:
                    s = nums[n1] + nums[n2] + nums[n3] + nums[n4]
                    if s < target:
                        n3 += 1
                    elif s > target:
                        n4 -= 1
                    else:  # 相等，继续
                        ans.append([nums[n1], nums[n2], nums[n3], nums[n4]])
                        while n3 < n4 and nums[n3] == nums[n3 + 1]:
                            n3 += 1
                        while n3 < n4 and nums[n4] == nums[n4 - 1]:
                            n4 -= 1
                        n3 += 1  # 继续后移、前移，比如 2356 的情况，要找 8 找到 26 继续找 35
                        n4 -= 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
