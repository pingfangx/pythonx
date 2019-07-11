from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class InsertionSort(BaseSort):
    """插入排序"""

    def sort(self, a: List) -> List:
        for i in range(1, len(a)):  # i 作为要查找插入的值
            t = a[i]  # 值
            j = i  # 开始比较的数
            while j > 0 and t < a[j - 1]:
                # 如果t小，则值向后移
                a[j] = a[j - 1]
                j -= 1
            # 当退出循环时，j 为 0 或者 t 比 a[j-1] 大
            a[j] = t
        return a

    def sort2(self, a: List) -> List:
        for i in range(1, len(a)):  # i 作为要查找插入的值
            x = a[i]  # 值
            j = i - 1  # 开始比较的数
            while j >= 0 and x < a[j]:
                # 如果x小，则值向后移
                a[j + 1] = a[j]
                j -= 1
            # 当退出循环时，j 为 -1 或者 x 比 a[j] 大，所以加1
            a[j + 1] = x
        return a

    def sort1(self, a: List) -> List:
        """这是找到位置才排序，直接应该边找边排"""
        for i in range(1, len(a)):  # 第一个认为已经排好序
            x = a[i]
            j = i
            while j > 0 and x < a[j - 1]:
                j -= 1
            # 要让退出时 j=0，所以使用的 >0 和 [j-1]
            a[j + 1:i + 1] = a[j:i]  # 后移
            a[j] = x  # 插入

        return a


class _Test(BaseSortTest):
    sort_class = InsertionSort
