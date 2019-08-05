class Solution:
    def isValid(self, s: str) -> bool:
        """
        成对出现，栈中只保存左括号
        遇到右括号时，如果栈为空，或者 pop 不等于左括号，则失败

        1
        答案的字典与我的相反，不改了，优化下语句
        >>> Solution().isValid('')
        True
        >>> Solution().isValid('()')
        True
        >>> Solution().isValid('([{}])')
        True
        >>> Solution().isValid(')')
        False
        """
        stack = []
        symbols = {
            '(': ')',
            '[': ']',
            '{': '}',
        }
        values = symbols.values()
        for c in s:
            if c in symbols:
                stack.append(c)
            elif c in values:
                if not stack or symbols[stack.pop()] != c:
                    return False
            else:
                return False
        return len(stack) == 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
