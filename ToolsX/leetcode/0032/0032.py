class Solution:
    """20190801"""

    def longestValidParentheses(self, s: str) -> int:
        """
        之前的 0022 是生成括号
        首先考虑用栈
        >>> Solution().longestValidParentheses('(()')
        2
        >>> Solution().longestValidParentheses(')()())')
        4
        """
        n = len(s)
        ans = 0
        for i in range(n - 1):
            stack = []
            left = i
            for j in range(i, n):
                if len(stack) == 0:
                    if s[j] == '(':  # 为空时只添加左括号
                        stack.append(s[j])
                    else:
                        left = j + 1  # 这里其实应该 break 见 0032_1
                else:
                    if s[j] == '(':
                        stack.append(s[j])
                    else:
                        stack.pop()
                        if len(stack) == 0:
                            ans = max(ans, j - left + 1)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
