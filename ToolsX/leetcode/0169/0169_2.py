from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        只能想到累计

        1
        答案真棒，虽然和我一样的算法，但相关方法不熟练

        2
        确定 Majority Element 的定义
        """
        return sorted(nums)[len(nums) // 2]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
