class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        """好像除了 kmp 没人讨论优化"""
        if not needle:
            return 0
        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i:i + len(needle)] == needle:
                return i
        return -1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
