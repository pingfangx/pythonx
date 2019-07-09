from typing import List

from leetcode import ListFactory


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        可以双循环，但是 T(n)=O(n^2) 感觉肯定过不了
        想到可以遍历一遍，每个数 - target 但好像没什么用

        1
        原本的好像没什么用好像也是可用的，因为如果 a+b=target
        用 target- 就会得到 target-a target-b 也就是说减一遍之后变成了找相同元素。
        但这样好像只是将 + 的计算从 n^2/2 变为 n
        但是 ==  的判断依然在
        且空间复杂度变为了 O(n)

        >>> Solution().twoSum(ListFactory.create(),-1)
        []
        >>> Solution().twoSum(ListFactory.create(),9)
        [3, 4]
        """
        dif = [target - i for i in nums]
        length = len(nums)
        for i in range(length - 1):
            for j in range(i + 1, length):
                if nums[i] == dif[j]:
                    return [i, j]
        return []


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
