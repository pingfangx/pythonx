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


        >>> Solution().generateParenthesis(3)
        """

        t = []
        ans = []

        def generate():
            if len(t) == 2 * n:
                if valid(t):
                    ans.append(''.join(t))
            else:

                t.append('(')  # 添加左括号
                generate()
                t.pop()  # 移除
                t.append(')')  # 添加右括号
                generate()
                t.pop()

        def valid(s):
            b = 0
            for i in s:
                if i == '(':
                    b += 1
                else:
                    b -= 1
                if b < 0:
                    return False
            return b == 0

        generate()
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
