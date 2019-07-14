from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """
        中位数（又称中值，英语：Median），统计学中的专有名词，代表一个样本、种群或概率分布中的一个数值，其可将数值集合划分为相等的上下两部分。
        理解中位数，一个有序列表中中间的一个元素，或中间的两个元素的平均值
        现在的问题是两个有序列表，而不是一个

        如果是偶数，记录前一个和当前


        假设合并后数组为奇数
            1   2   3
        mid=1，应取到 <=mid
        pre cur
            pre cur
        返回 cur

        假设合并后数组为偶数
            1   2   3   4
        mid 应取为 2，取到 <=mid
        pre cur
            pre cur
                pre cur
        返回 (pre+cur)/2

        >>> Solution().findMedianSortedArrays([1],[2])
        1.5
        >>> Solution().findMedianSortedArrays([1, 3],[2])
        2
        >>> Solution().findMedianSortedArrays([1, 2],[3, 4])
        2.5
        """
        n1 = len(nums1)
        n2 = len(nums2)
        n = n1 + n2
        mid = n >> 1

        cur = pre = i = j = k = 0
        while i < n1 and j < n2 and k <= mid:  # 因为要取到 mid 处的值，所以取 <=
            if nums1[i] <= nums2[j]:
                pre, cur = cur, nums1[i]
                i += 1
                k += 1
            else:
                pre, cur = cur, nums2[j]
                j += 1
                k += 1
        # 如果某个数组结束，继续迭代另一个数组
        while k <= mid and i < n1:
            pre, cur = cur, nums1[i]
            i += 1
            k += 1
        while k <= mid and j < n2:
            pre, cur = cur, nums2[j]
            k += 1
            j += 1
        # 结束时 k=mid，判断奇偶
        if n & 1 == 0:  # 偶数，求平均值
            return (pre + cur) / 2
        else:
            return cur


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
