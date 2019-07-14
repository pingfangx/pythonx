import math
from typing import List

from leetcode import ListFactory
from leetcode.algorithm.sort import BaseSort, BaseSortTest


class RadixSort(BaseSort):
    """基数排序"""

    def sort(self, a: List, radix=10) -> List:
        k = int(math.ceil(math.log(max(a), radix)))
        for i in range(1, k + 1):
            bucket = [[] for _ in range(radix)]
            for j in a:
                # 例如 12，12%10//1
                index = j % (radix ** i) // (radix ** (i - 1))
                bucket[index].append(j)
            a.clear()  # 清空 a
            for j in bucket:  # 放回 a 中
                a += j
        return a


class _Test(BaseSortTest):
    sort_class = RadixSort

    def generate_test_list(self) -> List:
        return ListFactory.from_iter([101, 12, 7, 5, 4, 0])
