from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        遍历是入门，先写一遍
        >>> Solution().threeSum([-1, 0, 1, 2, -1, -4])
        [[-1, 0, 1], [-1, -1, 2]]
        >>> Solution().threeSum([3,0,-2,-1,1,2])
        [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
        """
        n = len(nums)
        if n < 3:
            return []
        ans = []
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        t = sorted([nums[i], nums[j], nums[k]])
                        if t not in ans:
                            ans.append(t)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
