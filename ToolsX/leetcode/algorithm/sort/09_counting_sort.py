from typing import List

from leetcode.algorithm.sort import BaseSort, BaseSortTest


class CountingSort(BaseSort):
    """计数排序"""

    def sort(self, a: List) -> List:
        """为了减小空间，求最小最大"""
        min_v = min(a)
        max_v = max(a)
        k = max_v - min_v + 1
        ans = [0] * len(a)  # 要取 a 的长度，比如有相同元素
        c = [0] * k  # 因为用数字作索引，所以多一位
        for i in a:
            c[i - min_v] += 1  # 统计次数,c[i] 表示 i 出现了多少次
        for i in range(1, k):
            c[i] += c[i - 1]  # 统计小于它的数
        for i in range(len(a) - 1, -1, -1):
            value = a[i]  # 数字
            count = c[value - min_v]  # 小于等于 value 的有 c[value] 个
            ans[count - 1] = value  # 放在 count-1 处
            # -1 如果还有等于 value 的元素，放在前面，这也是为什么要倒序
            # 这样相同元素，靠后的先排，相等的在下次迭代时前移
            c[value - min_v] -= 1
        return ans

    def sort1(self, a: List) -> List:
        k = max(a)
        ans = [0] * k
        c = [0] * (k + 1)  # 因为用数字作索引，所以多一位
        for i in a:
            c[i] += 1  # 统计次数,c[i] 表示 i 出现了多少次
        for i in range(1, k + 1):
            c[i] += c[i - 1]  # 统计小于它的数
        for i in range(len(a) - 1, -1, -1):
            value = a[i]  # 数字
            count = c[value]  # 小于等于 value 的有 c[value] 个
            ans[count - 1] = value  # 放在 count-1 处
            # -1 如果还有等于 value 的元素，放在前面，这也是为什么要倒序
            # 这样相同元素，靠后的先排，相等的在下次迭代时前移
            c[value] -= 1
        return ans


class _Test(BaseSortTest):
    sort_class = CountingSort

    def generate_test_list(self) -> List:
        return [52, 51, 50, 50, 50]
