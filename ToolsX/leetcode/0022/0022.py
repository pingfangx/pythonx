from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        不正确，好像总是不全
        >>> Solution().generateParenthesis(4)
        """
        if n < 1:
            return []
        elif n == 1:
            return ['()']
        else:
            result = []
            pre = self.generateParenthesis(n - 1)
            for s in pre:
                result.append('(' + s + ')')  # 包围
                prefix = '()' + s
                if prefix not in result:  # 前
                    result.append(prefix)
                suffix = s + '()'
                if suffix not in result:
                    result.append(s + '()')  # 后
                if n & 1 == 0:  # 偶数
                    double = self.generate(n // 2) * 2
                    if double not in result:
                        result.append(double)
            result.sort()  # 排序便于与结果比对
            return result

    def generate(self, n):
        r = ''
        for _ in range(n):
            r = '(' + r + ')'
        return r


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
