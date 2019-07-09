class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        """最后的单词

        就是要注意空格
        可能是单个字母
        可能是单个字母末尾加空格

        计论中还用使用 split 的，我觉得 find 之类的方法是将循环简化，不使用也可以手写，split 就不好了。
        >>> Solution().lengthOfLastWord('a ')
        1
        """
        s = s.strip()
        rindex = s.rfind(' ')
        return len(s) if rindex == -1 else len(s) - rindex - 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
