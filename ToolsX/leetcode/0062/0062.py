from typing import List


class Solution:
    """20190827"""

    def uniquePaths(self, m: int, n: int) -> int:
        """
        喜欢这样的题

        该解法记录了路径，如果不需要路径，可以只记录数量就可以了
        但是超时，想一想，想不出来，好像可以直接计算，但是我的思维可能还差一点
        28 的时候为 7+6+5+4+3+2+1
        >>> Solution().uniquePaths(3,2)
        3
        >>> Solution().uniquePaths(7,3)
        28
        """
        paths = []
        self.unique_path(paths, [], (1, 1), (n, m))  # 注意是 1,1 不是 0,0 是 n,m 不是 m,n
        # print(paths)
        return len(paths)

    def unique_path(self, paths: List[str], steps: List[str], start, finish):
        if start == finish:
            paths.append(' -> '.join(steps))
        if self.can_right(start, finish):
            self.unique_path(paths, steps + ['Right'], (start[0], start[1] + 1), finish)
        if self.can_down(start, finish):
            self.unique_path(paths, steps + ['Down'], (start[0] + 1, start[1]), finish)

    def can_right(self, start, finish) -> bool:
        return start[1] < finish[1]

    def can_down(self, start, finish) -> bool:
        return start[0] < finish[0]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
