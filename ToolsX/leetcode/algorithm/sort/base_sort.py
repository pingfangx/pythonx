import sys
import unittest
from typing import List

from leetcode import ListFactory


class BaseSort:
    """排序基类"""

    def sort(self, a: List) -> List:
        """排序"""
        raise NotImplementedError(f'{self.__class__.__name__}.{sys._getframe().f_code.co_name} not implemented')


class BaseSortTest(unittest.TestCase):
    """排序测试"""
    sort_class = BaseSort
    """排序类"""

    def test_sort(self):
        """测试排序"""
        source = self.generate_test_list()
        result = self.sort(source.copy())
        self.assertListEqual(sorted(source), result)

    def generate_test_list(self) -> List:
        """生成测试列表"""
        return ListFactory.from_num(54321)

    def sort(self, a: List) -> List:
        """执行排序"""
        if self.sort_class:
            return self.sort_class().sort(a)
        return a
