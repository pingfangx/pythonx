class Solution:
    """20190902"""

    def minDistance(self, word1: str, word2: str) -> int:
        """
        hard 难度，感觉不太好解决
        先考虑变为一样长度的，再比较
        但是存在一样长度的，也可能先删除，再添加的情况

        1
        https://leetcode.com/problems/edit-distance/discuss/159295/Python-solutions-and-intuition

        2
        方法是好方法，可惜不一定我能想出来

        >>> Solution().minDistance('sea','eat')
        2
        >>> Solution().minDistance('intention','execution')
        5
        """
        m = len(word1)
        n = len(word2)
        table = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            table[i][0] = i
        for j in range(n + 1):
            table[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    table[i][j] = table[i - 1][j - 1]
                else:
                    table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
        return table[-1][-1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
