class Solution:
    """20190906"""

    def minWindow(self, s: str, t: str) -> str:
        """难
        一开始想差，从最多的开始判断，如果满足，就依次减小
        但是可能多部分都是满足的，减小会无法找到最短的

        >>> Solution().minWindow('ADOBECODEBANC','ABC')
        'BANC'
        >>> Solution().minWindow('cabwefgewcwaefgcf','cae')
        'cwae'
        """
        ans1 = ''
        p = s
        while self.is_valid(p, t):
            ans1 = p
            p = p[1:]
        p = ans1
        while self.is_valid(p, t):
            ans1 = p
            p = p[:-1]

        return ans1

    def is_valid(self, s: str, t: str) -> bool:
        a1 = [i for i in s]
        a2 = [i for i in t]
        while a2:
            t = a2.pop()
            if t in a1:
                a1.remove(t)
            else:
                return False
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
