from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class HeapSort(BaseSort):
    def sort(self, a: List) -> List:
        def max_heapify(start, end):
            parent = start
            while True:
                # 以 0 为起点，相当于 parent*2 +1
                child = (parent + 1) * 2 - 1  # child 为索引
                if child > end:
                    break
                if child + 1 <= end and a[child] < a[child + 1]:
                    child += 1  # 若右结点较大，取右结点
                if a[parent] < a[child]:  # parent 是否比 child 小
                    a[parent], a[child] = a[child], a[parent]  # 如果小，则交换，继换看 child（视为 parent 迭代）
                    parent = child
                else:  # 如果 parent >= child 说明最大堆符合要求，跳出
                    break

        n = len(a)
        # 创建最大堆
        # 为什么取一半就行？考虑最下面一层是叶子结点，只需从非叶子节点开始即可，max_heapify 中会与子结点比较
        # 因为是从 0 开始的 n//2 得到一半，再 -1 得到 index
        # 会什么倒序？考虑多层，依次向上直至 root
        for i in range(n // 2 - 1, -1, -1):
            max_heapify(i, n - 1)  # i 到最后
        # 最大堆生成完成，进行堆排序
        for i in range(n - 1, 0, -1):  # [n-1,0) 到 1 停止，因为要调整 i-1
            # 将最大的换到最后
            a[0], a[i] = a[i], a[0]
            # 重新调整最大之前的
            max_heapify(0, i - 1)
        return a


class _Test(BaseSortTest):
    sort_class = HeapSort
