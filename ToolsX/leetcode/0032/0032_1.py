class Solution:
    """20190801"""

    def longestValidParentheses(self, s: str) -> int:
        """
        之前的 0022 是生成括号
        首先考虑用栈

        1
        不需要用栈，考虑计数

        >>> Solution().longestValidParentheses('(()')
        2
        >>> Solution().longestValidParentheses(')()())')
        4
        """
        n = len(s)
        ans = 0
        for i in range(n - 1):
            count = left = 0
            for j in range(i, n):
                if count == 0:
                    if s[j] == '(':
                        count += 1
                    else:
                        left = j + 1
                else:
                    if s[j] == '(':
                        count += 1
                    else:
                        count -= 1
                        if count == 0:
                            ans = max(ans, j - left)
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
