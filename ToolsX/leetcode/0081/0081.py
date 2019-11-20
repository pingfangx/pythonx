from typing import List


class Solution:
    """20190911"""

    def search(self, nums: List[int], target: int) -> bool:
        """前一题是 0033，不想做这一题"""
        return target in nums


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
