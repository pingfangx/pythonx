class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        路上思考了一下，有点难
        首先试一下没有使用 . 只使用 * 的情况
        递归时会创建多个字符串，占用更多空间，但是为了便于理解和简化操作，还是直接截取

        1
        加上 . 补充判断
        >>> Solution().isMatch('aaa','ab*a*c*a')
        True
        >>> Solution().isMatch('','')
        True
        >>> Solution().isMatch('a','')
        False
        >>> Solution().isMatch('','a')
        False
        >>> Solution().isMatch('','.')
        False
        >>> Solution().isMatch('','.*')
        True
        >>> Solution().isMatch('a','*')
        False
        >>> Solution().isMatch('a','a*')
        True
        >>> Solution().isMatch('abbc','ab*c*')
        True
        >>> Solution().isMatch('a','.')
        True
        >>> Solution().isMatch('ab','a.')
        True
        >>> Solution().isMatch('ab','.*')
        True
        >>> Solution().isMatch('abc','a.*')
        True
        >>> Solution().isMatch('aab','c*a*b')
        True
        >>> Solution().isMatch('aaa','ab*a*c*a')
        True
        """
        # 取最后一个模式字符
        if not s and not p:  # 同时为空，匹配成功
            return True
        elif not p:  # 模式就为空，字符为不为空，失败
            return False
        elif not s:  # 字符为空，模式不为空
            if len(p) >= 2 and p[-1] == '*':  # 匹配任意
                return self.isMatch(s, p[:-2])
            else:
                return False
        # 都不为空，开始匹配
        last = p[-1]
        if last == '*':  # 匹配 *
            if len(p) > 1:  # 模式长度大于1，匹配 n 个前一个字符
                pre = p[-2]
                if pre == '.':  # .*
                    if len(p) > 2:  # 长度大于2，看 .* 前面是什么
                        if self.isMatch(s, p[:-2]):
                            return True
                        while s:
                            s = s[:-1]
                            if self.isMatch(s, p[:-2]):
                                return True
                        return False
                    else:  # 长度小于2，.* 匹配
                        return True
                else:
                    # 将最后的前一个字符清空，或者直接不处理，因为 * 可以匹配 0 个
                    if self.isMatch(s, p[:-2]):
                        return True
                    while s and s.endswith(pre):  # 依次减少一个，看是否匹配
                        s = s[:-1]
                        if self.isMatch(s, p[:-2]):
                            return True
                    return False
            else:  # 模式为单独的 *
                return False
        elif last == '.':  # 匹配 .
            return self.isMatch(s[:-1], p[:-1])
        else:  # 正常字符
            if s[-1] == last:  # 字符匹配，将其删除，继续匹配
                return self.isMatch(s[:-1], p[:-1])
            else:  # 字符不匹配
                return False


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
