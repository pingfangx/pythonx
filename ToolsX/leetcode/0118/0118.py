from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        """
        递归直接超限了
        >>> Solution().generate(5)[-1]
        [1, 4, 6, 4, 1]
        """
        if numRows == 1:
            return [[1]]
        else:
            triangle = self.generate(numRows - 1)
            line = triangle[-1]
            a = [1]
            # 第一和最后都是 1 中间是上一层相加
            for i in range(1, numRows - 1):
                a.append(line[i - 1] + line[i])
            a.append(1)
            triangle.append(a)
            return triangle


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
