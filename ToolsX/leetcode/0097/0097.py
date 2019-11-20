from typing import List


class Solution:
    """20190925"""

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        """
        交错，先来一个暴力美学
        将后者依次插入前者
        插入的过程想到一种思路，只要能找到后者的所有字母，就代表交错
        >>> Solution().isInterleave('aabcc','dbbca','aadbbcbcac')
        True
        >>> Solution().isInterleave('aabcc','dbbca','aadbbbaccc')
        False
        """
        ans = []
        self.insert(ans, list(s1), list(s2), 0)
        return s3 in ans

    def insert(self, ans: List[str], chars1: List[str], chars2: List[str], start: int):
        if not chars2:
            ans.append(''.join(chars1))
            return
        n = len(chars1)
        c = chars2.pop(0)
        for i in range(start, n + 1):
            chars1.insert(i, c)  # 插入
            self.insert(ans, chars1, chars2, i + 1)
            chars1.pop(i)  # 移除
        chars2.insert(0, c)  # 结束后要还原，上一层还要继续处理


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
