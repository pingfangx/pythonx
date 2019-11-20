class Solution:
    """20190830"""

    def isNumber(self, s: str) -> bool:
        """
        hard 难度，先用正则试一下，通过了再根据正则的判断手动判断
        各种特殊情况，提交的时候判断
        为什么是 hard 难度，因为各种情况，烦死人
        >>> Solution().isNumber(' 0.1 ')
        True
        >>> Solution().isNumber('abc')
        False
        >>> Solution().isNumber('1 a')
        False
        >>> Solution().isNumber('2e10')
        True
        >>> Solution().isNumber(' -90e3   ')
        True
        >>> Solution().isNumber(' 1e')
        False
        >>> Solution().isNumber('e3')
        False
        >>> Solution().isNumber(' 6e-1')
        True
        >>> Solution().isNumber(' 99e2.5 ')
        False
        >>> Solution().isNumber('53.5e93')
        True
        >>> Solution().isNumber(' --6 ')
        False
        >>> Solution().isNumber('-+3')
        False
        >>> Solution().isNumber('95a54e53')
        False
        """
        s = s.strip(' ')  # 去除空格
        if s.startswith('+') or s.startswith('-'):  # 去掉符号
            s = s[1:]
        if len(s) > 1 and s[0] in '.+-' and s[1] in ' .+-':  # 去掉符号后仍有多个非数字相连
            return False
        if s.count('.') > 1:  # 去掉开头的点
            return False
        if s.startswith('.'):  # 点只去除一次，如果存在多个则不正确
            s = s[1:]

        if s.count('e') > 1:  # 去掉 e
            return False
        e_index = s.find('e')
        if e_index >= 0:
            left = s[0:e_index]
            right = s[e_index + 1:]
            if ' ' in left or ' ' in right or '.' in right:
                return False
            return self.isNumber(left) and self.isNumber(right)

        if s.endswith('.'):  # 去掉末尾的点，在 e 的判断之后
            s = s[:-1]
        if not s:
            return False
        ans = True
        for i in s:
            if i == '.':
                continue
            ans = ans and (ord('0') <= ord(i) <= ord('9'))
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
