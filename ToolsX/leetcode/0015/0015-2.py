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
        >>> Solution().threeSum([-1, 0, 1, 2, -1, -4])
        [[-1, 0, 1], [-1, -1, 2]]
        >>> Solution().threeSum([0,0,0])
        [[0, 0, 0]]
        """
        n = len(nums)
        if n < 3:
            return []
        answer = []
        for i in range(n - 2):
            n1 = nums[i]
            # 有了 n1 在后续的数字中，寻找是否有两个数，其和为 n1 的相反数
            sums = {}  # 使用集合表示 hash map
            for j in range(i + 1, n):
                n2 = nums[j]
                if n2 in sums:
                    t = sorted([n1, n2, 0 - n1 - n2])
                    if t not in answer:
                        answer.append([n1, n2, 0 - n1 - n2])
                else:  # 寻找一个数，它与 n2 的和为 n1 的相反数
                    sums[0 - n1 - n2] = ''
        return answer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
