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

        2
        看了答案再来，已经想到差了，但是差就差在还差一点
        将 T(n) 变为 O(n)
        >>> Solution().twoSum(ListFactory.create(),-1)
        []
        >>> Solution().twoSum(ListFactory.create(),9)
        [3, 4]
        """
        # 记录差和 index
        dif = {}
        for i in range(len(nums)):
            if nums[i] in dif:
                return [dif[nums[i]], i]
            else:
                dif[target - nums[i]] = i
        return []


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
