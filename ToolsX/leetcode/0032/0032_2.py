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

        >>> Solution().longestValidParentheses('(()')
        2
        >>> Solution().longestValidParentheses(')()())')
        4
        >>> Solution().longestValidParentheses('()(()')
        2
        """
        n = len(s)
        ans = 0
        for i in range(n - 1):
            left = right = 0
            for j in range(i, n):
                if s[j] == '(':
                    left += 1
                else:
                    right += 1
                    if left == right:  # 左括号多，说明右括号可以配对相同数量的左括号
                        ans = max(ans, right + right)
                    elif left < right:  # 右括号多，错误
                        break
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
