class Solution:
    """20190906"""

    def minWindow(self, s: str, t: str) -> str:
        """难
        一开始想差，从最多的开始判断，如果满足，就依次减小
        但是可能多部分都是满足的，减小会无法找到最短的

        1
        看了解答，修改了思路，虽然超时，但总算能实现

        >>> Solution().minWindow('cabwefgewcwaefgcf','cae')
        'cwae'
        """
        ans = ''
        left = right = 0
        length = len(s)
        while left < length and right < length:
            right = left + 1
            while right < length and not self.is_valid(s[left:right], t):
                right += 1
            while self.is_valid(s[left:right], t):
                if ans == '' or len(s[left:right]) < len(ans):
                    ans = s[left:right]
                left += 1
        return ans

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
