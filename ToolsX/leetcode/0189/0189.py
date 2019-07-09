from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(k):
            nums[0], nums[1:] = nums[-1], nums[:-1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
