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


        1
        答案和讨论都是以下解法，但是实在有点难懂

        >>> Solution().findMedianSortedArrays([3, 4],[1, 2])
        2.5
        >>> Solution().findMedianSortedArrays([1, 2],[3, 4])
        2.5
        """

        # 根据介绍，要将 nums1 nums2 划分为两部分，使两部分长度相等，且左边最大值小于右边最小值
        m, n = len(nums1), len(nums2)
        if m > n:
            # 交换是为了 j = half_len - i，如果 m 是较大者，j 可能取到负
            nums1, nums2, m, n = nums2, nums1, n, m
        if n == 0:
            raise ValueError

        # i=0 ~ m，j=half_len -i 因为根据之前的分析，要分为左右长度相等的两部分，所以 j 等一半减 i
        imin, imax, half_len = 0, m, (m + n + 1) // 2
        while imin <= imax:
            i = (imin + imax) // 2
            j = half_len - i
            if i < m and nums2[j - 1] > nums1[i]:
                # i 在 m 内，但是 nums1[i] 太小了，需要 i 往后移
                imin = i + 1
            elif i > 0 and nums1[i - 1] > nums2[j]:
                # numbs[i] 太大了，需要 i 往前移
                imax = i - 1
            else:
                # i is perfect

                if i == 0:
                    #        |3  4
                    # 1     2|
                    # i 移到 0 说明 nums1 中都是较多数，从 nums2 中取中位数
                    max_of_left = nums2[j - 1]
                elif j == 0:
                    # 1     2|
                    #        |3     4
                    # 从 nums1 中取中位数
                    max_of_left = nums1[i - 1]
                else:
                    # 1|    3
                    # 2|    4
                    # 分为两半，左边取两者较大者
                    max_of_left = max(nums1[i - 1], nums2[j - 1])

                if (m + n) & 1 == 1:
                    # 奇数
                    return max_of_left

                if i == m:
                    # 1     2|
                    #        |3     4
                    # i 到底了，说明 nums1 中都是较小的，从 nums2 中取
                    min_of_right = nums2[j]
                elif j == n:
                    #        |3  4
                    # 1     2|
                    # j 到底，说明 nums2 中都是较小的，从 nums1 中取
                    min_of_right = nums1[i]
                else:
                    # 1|    3
                    # 2|    4
                    # 取较小者
                    min_of_right = min(nums1[i], nums2[j])

                return (max_of_left + min_of_right) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
