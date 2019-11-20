class Solution:
    """20190902"""

    def minDistance(self, word1: str, word2: str) -> int:
        """
        hard 难度，感觉不太好解决
        先考虑变为一样长度的，再比较
        但是存在一样长度的，也可能先删除，再添加的情况

        1
        https://leetcode.com/problems/edit-distance/discuss/159295/Python-solutions-and-intuition

        >>> Solution().minDistance('sea','eat')
        2
        >>> Solution().minDistance('intention','execution')
        5
        """
        return self.min_distance(word1, word2, {})

    def min_distance(self, word1: str, word2: str, cache: dict) -> int:
        if not word1 and not word2:
            return 0
        if not word1:
            return len(word2)
        if not word2:
            return len(word1)
        if word1[0] == word2[0]:
            return self.min_distance(word1[1:], word2[1:], cache)
        if (word1, word2) not in cache:
            insert = 1 + self.min_distance(word1, word2[1:], cache)
            delete = 1 + self.min_distance(word1[1:], word2, cache)
            replace = 1 + self.min_distance(word1[1:], word2[1:], cache)
            cache[(word1, word2)] = min(insert, replace, delete)
        return cache[(word1, word2)]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
