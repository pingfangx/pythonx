import random
from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class QuickSort(BaseSort):
    """快速排序"""

    def swap(self, a: List, x: int, y: int):
        a[x], a[y] = a[y], a[x]

    def partition(self, a: List, left: int, right: int):
        p_index = random.randrange(left, right)
        p_value = a[p_index]

        self.swap(a, p_index, right)  # 移到最后
        s_index = left
        for i in range(left, right):
            if a[i] < p_value:
                self.swap(a, i, s_index)  # i 小，交换到前面
                s_index += 1
        self.swap(a, right, s_index)  # 将中间值交换回去
        return s_index

    def sort(self, a: List, left=0, right=None) -> List:
        if right is None:
            right = len(a) - 1
        if left >= right:
            return a
        t = self.partition(a, left, right)
        self.sort(a, left, t - 1)
        self.sort(a, t + 1, right)
        return a

    def sort1(self, a: List) -> List:
        if len(a) <= 1:
            return a
        left, mid, right = [], [], []
        pivot = random.choice(a)
        for i in a:
            if i < pivot:
                left.append(i)
            elif i == pivot:
                mid.append(i)
            else:
                right.append(i)
        return self.sort(left) + mid + self.sort(right)


class _Test(BaseSortTest):
    sort_class = QuickSort
