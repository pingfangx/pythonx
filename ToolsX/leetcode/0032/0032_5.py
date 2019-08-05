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

        5 也是使用 left right ，如 0032_2，但是自己完成不了，原来只需要再反向一遍就可以了
        第一遍可以处理 ()()))
        第二遍可以处理 (((((()()

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
        left = right = 0
        for i in range(n):
            if s[i] == '(':
                left += 1
            else:
                right += 1
                # 该判断放在 else 中，因为增加 left 不可能平衡，只有增加 right 才可能会由不平衡变为平衡
                if left == right:  # 左括号多，说明右括号可以配对相同数量的左括号
                    ans = max(ans, right * 2)
                elif left < right:  # 右括号多，错误
                    left = right = 0
        left = right = 0
        for i in range(n - 1, -1, -1):
            if s[i] == ')':
                right += 1
            else:
                left += 1
                if left == right:
                    ans = max(ans, left * 2)
                elif right < left:
                    left = right = 0
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
