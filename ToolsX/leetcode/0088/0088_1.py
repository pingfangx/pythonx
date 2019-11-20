from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        使用两个指针

        1 可以递减，不需要 insert 再 del
        而是直接放在数组末尾填充过来
        因为 m 和 n 都表示 length 所以在用于索引时都有 -1 的处理
        >>> nums1=[1,2,3,0,0,0]
        >>> Solution().merge(nums1,3,[2,5,6],3)
        >>> nums1
        [1, 2, 2, 3, 5, 6]
        """
        while m > 0 and n > 0:
            if nums1[m - 1] >= nums2[n - 1]:
                # 大于，放在末尾
                nums1[m + n - 1] = nums1[m - 1]
                m -= 1
            else:
                # 要插入
                nums1[m + n - 1] = nums2[n - 1]
                n -= 1
        if n > 0:
            nums1[:n] = nums2[:n]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
