from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """还是使用两个指针尝试
        >>> Solution().threeSumClosest([1,1,-1,-1,3],-1)
        -1
        >>> Solution().threeSumClosest([-1, 2, 1, -4],1)
        2
        """
        n = len(nums)
        if n < 3:
            return 0

        nums.sort()
        min_dif = None
        ans = 0
        for i in range(n - 2):
            left = i + 1
            right = n - 1
            while left < right:
                s = nums[i] + nums[left] + nums[right]
                if s < target:
                    dif = target - s
                    if min_dif is None or dif < min_dif:
                        min_dif = dif
                        ans = s
                    left += 1
                elif s > target:
                    dif = s - target
                    if min_dif is None or dif < min_dif:
                        min_dif = dif
                        ans = s
                    right -= 1
                else:
                    return target
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
