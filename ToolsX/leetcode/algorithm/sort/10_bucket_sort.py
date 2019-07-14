from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class BucketSort(BaseSort):
    def sort(self, a: List) -> List:
        bucket_number = 10
        min_v = min(a)
        max_v = max(a)
        # 桶怎么分不太正确，网上示例不多，先这样吧，+1 保证 max 分到最后一桶，而不会越界
        step = (max_v + 1 - min_v) / bucket_number
        buckets = [[] for _ in range(bucket_number)]

        # 放入不同的桶中
        for i in a:
            index = int((i - min_v) / step)
            buckets[index].append(i)

        # 排序桶，也可以插入的时候就排序
        for i, bucket in enumerate(buckets):
            buckets[i] = sorted(bucket)  # 要使用稳定排序，这里直接用 sorted 偷懒

        # 放回原数组
        a.clear()
        for i in buckets:
            a += i
        return a


class _Test(BaseSortTest):
    sort_class = BucketSort

    def generate_test_list(self) -> List:
        return [100, 23, 23, 13, 0]
