from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        使用两个指针
        >>> nums1=[1,2,3,0,0,0]
        >>> Solution().merge(nums1,3,[2,5,6],3)
        >>> nums1
        [1, 2, 2, 3, 5, 6]
        """
        i = j = 0
        while i < m and j < n:
            if nums1[i] <= nums2[j]:
                # 已经在 num1 继续后移
                i += 1
            else:
                nums1.insert(i, nums2[j])  # 插入
                del nums1[-1]  # 删除最后的元素
                j += 1  # j 后移
                i += 1  # i 也要移动，因为插入了元素
                m += 1  # m 是 while 的判断，也要后移
        while j < n:  # 结束后添加剩余的
            nums1.insert(i, nums2[j])
            del nums1[-1]
            i += 1
            j += 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
