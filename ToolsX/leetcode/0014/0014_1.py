from typing import List


class Solution:

    def longestCommonPrefix(self, strs: List[str]) -> str:
        """
        按顺序比较就好了

        1
        看了答案后
        1,
        较慢的是水平扫描，第一个字符串，依次判断是否包含，不包含就减小长度

        2,
        本方法是垂直扫描

        3,分治
        分作两伴，查找再合并

        4,二分

        5,Trie
        """
        if not strs:
            return ''
        first = strs[0]

        buffer = ''
        for i in range(len(first)):
            c = first[i]
            for str in strs[1:]:
                # 不可能大于，== 的时候就 return 了
                if i == len(str) or str[i] != c:
                    return buffer
            # 所有的字符中都有 c 添加
            buffer += c
        return buffer


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
