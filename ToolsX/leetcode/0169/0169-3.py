from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        只能想到累计

        1
        答案真棒，虽然和我一样的算法，但相关方法不熟练

        2
        确定 Majority Element 的定义

        3
        Boyer–Moore majority vote algorithm
        多数投票算法
        当变为 0 的时候，认为他就是大多数
        """
        candidate = count = 0
        for n in nums:
            if count == 0:
                candidate = n
            if n == candidate:
                count += 1
            else:
                count -= 1
        return candidate


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
