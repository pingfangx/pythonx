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

        >>> Solution().generateParenthesis(3)
        """
        ans = []

        def generate(s='', left=0, right=0):
            if len(s) == 2 * n:  # 按正确的格式添加到指定长度
                ans.append(s)
                return
            if left < n:  # 再添加一个左括号
                generate(s + '(', left + 1, right)
            if right < left:  # 添加一个右括号
                generate(s + ')', left, right + 1)

        generate()
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
