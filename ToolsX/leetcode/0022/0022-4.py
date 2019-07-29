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

        2
        答案中的暴力穷举，要么加 ( 要么加 )，如果有效就返回

        3
        按正确的格式添加，不需要较验

        4
        只是抄一遍，我应该想不出这样的方法

        >>> Solution().generateParenthesis(3)
        """
        if n == 0:
            return ['']
        ans = []
        for i in range(n):
            for left in self.generateParenthesis(i):
                for right in self.generateParenthesis(n - i - 1):
                    ans.append(f'({left}){right}')  # left 和 right 可能为 '' 也可能为格式正确的括号组
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
