from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        遍历是入门，先写一遍

        1
        超时超时
        >>> Solution().threeSum([-1, 0, 1, 2, -1, -4])
        [[-1, 0, 1], [-1, -1, 2]]
        >>> Solution().threeSum([0,0,0])
        [[0, 0, 0]]
        """
        n = len(nums)
        if n < 3:
            return []
        answer = []
        sums = {}
        single_nums = []
        for i in range(n):
            n1 = nums[i]
            if n1 in sums:  # 说明有两个数相加得到 -n1
                t_sum = sums[n1]
                for n2, n3 in t_sum:  # 两者相加都得 -n1
                    t = sorted([n1, n2, n3])
                    if t not in answer:
                        answer.append(t)
            # 不管是否存在，都要再添加，可能与其他数字组合
            if n1 in single_nums:  # 已经存在
                n2 = n1
                dif = 0 - n1 - n2
                if dif in sums:
                    if (n1, n2) not in sums[dif]:
                        sums[dif].append((n1, n2))
                else:
                    sums[dif] = [(n1, n2)]
            else:
                for n2 in single_nums:  # 不存在，求出可能的和
                    dif = 0 - n1 - n2
                    if dif in sums:
                        if (n1, n2) not in sums[dif]:
                            sums[dif].append((n1, n2))
                    else:
                        sums[dif] = [(n1, n2)]
                single_nums.append(n1)
        return answer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
