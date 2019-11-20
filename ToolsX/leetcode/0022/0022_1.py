from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        不正确，好像总是不全

        1
        换成相加的
        2=0+2或1+1
        3=0+3 或 1+2 或 2+1

        能成功，但是很慢


        >>> Solution().generateParenthesis(3)
        """
        if n < 1:
            return []
        elif n == 1:
            return ['()']
        else:
            result = set()
            for i in range(0, n):
                if i == 0:
                    suffix = self.generateParenthesis(n - 1)
                    for s in suffix:
                        result.add('(' + s + ')')
                else:
                    suffix = self.generateParenthesis(n - i)
                    prefix = self.generateParenthesis(i)
                    for p in prefix:
                        for s in suffix:
                            result.add(p + s)
        return list(result)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
