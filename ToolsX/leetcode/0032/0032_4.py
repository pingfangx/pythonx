class Solution:
    """20190801"""

    def longestValidParentheses(self, s: str) -> int:
        """
        之前的 0022 是生成括号
        首先考虑用栈

        1
        不需要用栈，考虑计数

        2
        记录左右
        但是超时
        3 如何在一轮循环中完成
        失败，放弃

        4
        stack 保存的是 index

        >>> Solution().longestValidParentheses(')(((((()())()()))()(()))(')
        22
        >>> Solution().longestValidParentheses('(()')
        2
        >>> Solution().longestValidParentheses(')()())')
        4
        >>> Solution().longestValidParentheses('()(()')
        2
        """
        n = len(s)
        ans = 0
        stack = [-1]
        for i in range(n):
            if s[i] == '(':
                stack.append(i)
            else:
                stack.pop()
                if len(stack) == 0:
                    stack.append(i)
                else:
                    ans = max(ans, i - stack[-1])  # 为什么可以直接减，因为减的是去除成对后的前一个，也就是不在配对中的
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
