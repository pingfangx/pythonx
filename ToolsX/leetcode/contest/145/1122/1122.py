from typing import List


class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        """

        >>> arr1 = [2,3,1,3,2,4,6,7,9,2,19]
        >>> arr2 = [2,1,4,3,9,6]
        >>> Solution().relativeSortArray(arr1,arr2)
        [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]
        """
        ans = []
        for i in arr2:
            j = 0
            while j < len(arr1):
                if i == arr1[j]:
                    ans.append(arr1.pop(j))  # 添加相等的,j 不变
                else:
                    j += 1
        ans += sorted(arr1)  # 可以自己排序，这里不处理了
        return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
