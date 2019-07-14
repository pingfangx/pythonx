from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class SelectionSort(BaseSort):
    """选择排序"""

    def sort(self, a: List) -> List:
        for i in range(len(a)):
            t = i
            for j in range(i, len(a)):
                if a[j] < a[t]:
                    t = j
            if i != t:
                # 交换
                a[i], a[t] = a[t], a[i]
        return a


class _Test(BaseSortTest):
    sort_class = SelectionSort
