class Solution:
    """20190901"""

    def simplifyPath(self, path: str) -> str:
        """
        >>> Solution().simplifyPath('/a//b////c/d//././/..')
        '/a/b/c'
        """
        import re
        path = re.sub('/{2,}', '/', path)
        segments = path.split('/')
        folders = []
        for segment in segments:
            if segment == '.' or segment == '':  # current
                continue
            elif segment == '..':  # parent
                if len(folders) > 0:
                    folders.pop()
            else:
                folders.append(segment)
        return '/' + '/'.join(folders)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
