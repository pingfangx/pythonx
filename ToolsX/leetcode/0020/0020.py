class Solution:
    def isValid(self, s: str) -> bool:
        """
        成对出现，栈中只保存左括号
        遇到右括号时，如果栈为空，或者 pop 不等于左括号，则失败

        T(n)=O(n) 每次迭代一个字符
        S(n)=O(n) 可能将所有字符都加进 stack
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
        for c in s:
            if c in symbols.keys():
                stack.append(c)
            elif c in symbols.values():
                if len(stack) == 0 or symbols[stack.pop()] != c:
                    return False
            else:
                return False
        return len(stack) == 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
