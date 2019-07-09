import collections
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        只能想到累计

        1
        答案真棒，虽然和我一样的算法，但相关方法不熟练
        """
        c = collections.Counter(nums)
        # counter 继承字典，keys() 返回各元素，而 get() 返回指定元素出现的次数
        return max(c.keys(), key=c.get)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
