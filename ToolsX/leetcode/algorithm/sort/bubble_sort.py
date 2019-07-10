from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class BubbleSort(BaseSort):
    """冒泡"""

    def sort(self, a: List) -> List:
        """
        将大的换到后
        外层 0-length-1
        内层 0-i
        用 j 和 j+1 比较
        """
        length = len(a)
        for i in range(length):
            # 从 0 到最后，因为使用 j+1 所以需要 -1 前移
            for j in range(length - i - 1):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
        return a

    def sort_consider_change(self, a: List) -> List:
        length = len(a)
        for i in range(length):
            # 从 0 到最后，因为使用 j+1 所以需要 -1 前移
            swap = False
            for j in range(length - i - 1):
                if a[j] > a[j + 1]:
                    swap = True
                    a[j], a[j + 1] = a[j + 1], a[j]
            if not swap:  # 没有交换
                return a
        return a

    def sort1(self, a: List) -> List:
        """
        边界总是不好选取
        将小的换到前
        ①外层循环的选取
        从后向前比较，所以外层循环选为每一轮的终点，所以是从 0 到倒数每二个，所以是 range(length-1)
        ②内层循环的选取
        外层选了 0 到 -2，内层就选从 -1 到 i+1
        然后使用 j 和 j-1 来判断
        """
        length = len(a)
        for i in range(length - 1):  # 用来作为比较终点，这里不包含最后一个，倒数第二个
            for j in range(length - 1, i, -1):  # 从最后一个比到 i 的后一个，最后一轮是 [-1] 与 [-2] 比较，不再前移
                if a[j] < a[j - 1]:  # 与前一个比较
                    a[j], a[j - 1] = a[j - 1], a[j]
        return a


class _Test(BaseSortTest):
    sort_class = BubbleSort
