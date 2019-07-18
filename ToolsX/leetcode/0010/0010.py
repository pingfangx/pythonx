class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        路上思考了一下，有点难
        首先试一下没有使用 . 只使用 * 的情况
        递归时会创建多个字符串，占用更多空间，但是为了便于理解和简化操作，还是直接截取

        >>> Solution().isMatch('','')
        True
        >>> Solution().isMatch('a','')
        False
        >>> Solution().isMatch('','a')
        False
        >>> Solution().isMatch('','.')
        True
        >>> Solution().isMatch('','.*')
        True
        >>> Solution().isMatch('a','*')
        False
        >>> Solution().isMatch('a','a*')
        True
        >>> Solution().isMatch('abbc','ab*c*')
        True
        """
        # 取最后一个模式字符
        if not s and not p:  # 同时为空，匹配成功
            return True
        elif not p:  # 模式就为空，字符为不为空，失败
            return False
        elif not s:  # 字符为空，模式不为空
            if p == '.' or p == '.*':  # 匹配任意
                return True
            else:
                return False
        # 都不为空，开始匹配
        last = p[-1]
        if last == '*':  # 匹配 *
            if len(p) > 1:  # 模式长度大于1，匹配 n 个前一个字符
                pre = p[-2]
                s = s.rstrip(pre)  # 将最后的前一个字符清空
                p = p[:-2]
                return self.isMatch(s, p)
            else:  # 模式为单独的 *
                return False
        else:  # 正常字符
            if s[-1] == last:  # 字符匹配，将其删除，继续匹配
                s = s[:-1]
                p = p[:-1]
                return self.isMatch(s, p)
            else:  # 字符不匹配
                return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
