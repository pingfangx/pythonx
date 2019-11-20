class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """不包含重复字符的最长子字符串

        i∈[0,n)
            记录之前的最长串
            如果 s[i] 位于最长串中，最长串加 1
            否则最长串变为 s[i] 的首次出现位置到 i

        要注意
        选择在有重复字符的时候才赋值，那么退出循环时需要加上后面不重复的
        
        T(n)=O(n^2)
        最外情况，每个字符都需要判断，n-1 轮，内部比较 [1,n-1] 次

        2
        答案中的方法2，使用 hashset 除低判断是否存在的时间复杂度
        以 O(n) 的空间复杂度为代价，将时间复杂度降为 O(n)
        i j 两个指针向后移
        不包含时，j 后移，记录长度
        包含时,i 后移，直到将相同元素删除，然后 j 继续后移

        但是为什么比 0 中的方法慢，可能是因为 0 中不会每次都调用 put 和 max 方法

        3
        答案中的方法3，优化于2
        记录下字符的位置，这样就不需要迭代 i ，而是直接跳过
        时间复杂度由上一例中的 O(2n) 降为 O(n)
        2 中可能该问两遍元素，该方法中只会访问一遍
        >>> Solution().lengthOfLongestSubstring('abba')
        2
        >>> Solution().lengthOfLongestSubstring('')
        0
        >>> Solution().lengthOfLongestSubstring('a')
        1
        >>> Solution().lengthOfLongestSubstring('au')
        2
        >>> Solution().lengthOfLongestSubstring('aab')
        2
        >>> Solution().lengthOfLongestSubstring('abcabcbb')
        3
        >>> Solution().lengthOfLongestSubstring('bbbbb')
        1
        >>> Solution().lengthOfLongestSubstring('pwwkew')
        3
        """
        n = len(s)
        unique = {}  # 用字典比 array 好
        i = ans = 0
        for j in range(n):
            if s[j] in unique:
                # 这里取出 uniques[s[j]] 还需要与 i 比较，i 已经移到后面就忽略前面的元素
                i = max(i, unique[s[j]])  # 如果在，i 后移到指定位置
            ans = max(ans, j - i + 1)
            unique[s[j]] = j + 1  # 为什么不直接保存而要加 1，这样可以与默认 0 区分开
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
