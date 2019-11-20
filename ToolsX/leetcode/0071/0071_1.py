class Solution:
    """20190901"""

    def simplifyPath(self, path: str) -> str:
        """
        1
        其实不需要处理多个 //

        当然了，系统的方法是 os.path.normpath()
        >>> Solution().simplifyPath('/a//b////c/d//././/..')
        '/a/b/c'
        """
        s = []
        for i in path.split('/'):
            if i == '..':  # parent
                if len(s) > 0:
                    s.pop()
            elif i != '.' and i != '':
                s.append(i)
        return '/' + '/'.join(s)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
