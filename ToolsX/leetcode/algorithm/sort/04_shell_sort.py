from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class ShellSort(BaseSort):
    """希尔排序"""

    def sort(self, a: List) -> List:
        n = len(a)
        gap = n >> 1
        while gap:
            for i in range(gap, n):  # 按每个步长进行插入排序
                t = a[i]
                j = i
                # ==gap 也要比较，即 0 项 和 gap 项
                while j >= gap and a[j - gap] > t:
                    a[j] = a[j - gap]
                    j -= gap
                a[j] = t
            gap >>= 1
        return a


class _Test(BaseSortTest):
    sort_class = ShellSort
