from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        递归直接超限了，改用迭代
        要注意后面每一行的迭代，要在前后添加 1
        后续位置从前一行的 0 开始加，所以是 [j-1]+[j]
        
        时间复杂度为 O(numRows^2)

        2
        看了讨论，可以错位相加

        3
        使用 map

        >>> Solution().generate(5)[-1]
        [1, 4, 6, 4, 1]
        """
        if numRows <= 0:
            return []
        triangle = [[1]]
        for i in range(1, numRows):
            triangle.append(list(map(lambda x, y: x + y, [0] + triangle[-1], triangle[-1] + [0])))
        return triangle


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
