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
        pre = {}
        ans = left = right = t_right = 0
        for i in range(n):
            if s[i] == '(':
                left += 1
                t_right = 0  # 置为0
            else:
                right += 1
                t_right += 1
                if left >= right:  # 匹配
                    if left == right:
                        t = right + right
                    else:
                        t = t_right + t_right
                    j = i - t
                    while j >= 0 and j in pre:
                        t += pre[j]
                        j -= pre[j]
                    pre[i] = t  # 记录 i 之前共有 t 个符号可匹配
                    ans = max(ans, t)
                    if left == right:  # 如果成对匹配，则置空，这样后续的又重新计算，如果连接，会在 pre 中取值累加
                        left = right = 0
                else:  # 失败
                    left = right = 0
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
