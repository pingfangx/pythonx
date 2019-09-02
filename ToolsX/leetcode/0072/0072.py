class Solution:
    """20190902"""

    def minDistance(self, word1: str, word2: str) -> int:
        """
        hard 难度，感觉不太好解决
        先考虑变为一样长度的，再比较
        但是存在一样长度的，也可能先删除，再添加的情况

        >>> Solution().minDistance('sea','eat')
        2
        >>> Solution().minDistance('intention','execution')
        5
        """
        n1, n2 = len(word1), len(word2)
        ans = 0
        if n1 < n2:  # 插入
            for _ in range(n2 - n1):
                ans += 1
                min_distance = -1
                min_word = ''
                for i in range(len(word1) + 1):
                    t = word1[:i] + word2[i] + word1[i:]
                    distance = self.minDistance(t, word2)
                    if min_distance == -1 or distance < min_distance:
                        min_distance = distance
                        min_word = t
                word1 = min_word
        elif n1 > n2:  # 删除
            for _ in range(n1 - n2):
                ans += 1
                min_distance = -1
                min_word = ''
                for i in range(len(word1)):
                    t = word1[:i] + word1[i + 1:]
                    distance = self.minDistance(t, word2)
                    if min_distance == -1 or distance < min_distance:
                        min_distance = distance
                        min_word = t
                word1 = min_word
        for i in range(n2):  # 替换
            if word1[i] != word2[i]:
                ans += 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
