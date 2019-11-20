class Solution:
    """20190924"""

    def numTrees(self, n: int) -> int:
        """
        前一题是列出所有可能
        讨论中还有种种解法，可以参考
        >>> Solution().numTrees(3)
        5
        """
        if not n:
            return 0
        return self.num_trees({}, 1, n)

    def num_trees(self, cache: dict, start: int, end: int):
        if start > end:
            return 1
        res = 0
        if (start, end + 1) in cache:
            return cache[(start, end + 1)]
        for i in range(start, end + 1):
            left = self.num_trees(cache, start, i - 1)
            right = self.num_trees(cache, i + 1, end)
            res += left * right
        cache[(start, end + 1)] = res
        return res


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
