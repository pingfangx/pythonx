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
        或者因为 find 很快？
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
        i = j = ans = 0
        while i < n and j < n:
            if s[j] not in unique:  # 如果不包含，增加，j 后移,i 不变
                unique[s[j]] = ''
                j += 1
                ans = max(ans, j - i)
            else:
                del unique[s[i]]  # 如果包含，删除最前的元素， j 不变，i 后移，如果删除的元素不是重复元素，会继续判断删除
                i += 1
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
