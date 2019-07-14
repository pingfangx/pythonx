from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class MergeSort(BaseSort):
    def sort(self, a: List) -> List:
        result = [0] * len(a)
        self.merge_sort(a, result, 0, len(a) - 1)
        return result

    def merge_sort(self, a, result, start, end):
        if start >= end:
            return
        mid = start + ((end - start) >> 1)
        s1 = start
        e1 = mid
        s2 = mid + 1
        e2 = end
        self.merge_sort(a, result, s1, e1)
        self.merge_sort(a, result, s2, e2)
        k = start
        while s1 <= e1 and s2 <= e2:
            if a[s1] <= a[s2]:
                result[k] = a[s1]
                s1 += 1
            else:
                result[k] = a[s2]
                s2 += 1
            k += 1
        while s1 <= e1:
            result[k] = a[s1]
            k += 1
            s1 += 1
        while s2 <= e2:
            result[k] = a[s2]
            k += 1
            s2 += 1
        a[start:end + 1] = result[start:end + 1]  # 赋值给 a


class MergeSort1(BaseSort):
    """需要额外空间"""

    def sort(self, a: List) -> List:
        n = len(a)
        if n <= 1:
            return a
        else:
            mid = n >> 1
            left = self.sort(a[:mid])
            right = self.sort(a[mid:])
            return self._merge1(left, right)

    def _merge(self, left, right):
        i = j = 0
        ans = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                ans.append(left[i])
                i += 1
            else:
                ans.append(right[j])
                j += 1
        if i < len(left):
            ans.extend(left[i:])
        if j < len(right):
            ans.extend(right[j:])
        return ans

    def _merge1(self, left, right):
        """认为 left 和 right 可以修改"""
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        if left:
            result += left
        if right:
            result += right
        return result


class _Test(BaseSortTest):
    sort_class = MergeSort
