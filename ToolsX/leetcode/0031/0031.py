from typing import List


class Solution:
    """20190731"""

    def nextPermutation(self, nums: List[int]) -> None:
        """
        有一个只考虑结果，不考虑复杂度的暴力实现，按顺序列出所有可能
        >>> a=[0,0,4,2,1,0]
        >>> Solution().nextPermutation(a)
        >>> a
        [0, 1, 0, 0, 2, 4]

        """

        all_possible = self.get_all_possible(nums)
        num = self.list_to_num(nums)
        n = len(all_possible)
        i = 0
        while i < n and all_possible[i] <= num:
            i += 1
        if i < n:
            nxt = all_possible[i]
        else:
            nxt = all_possible[0]

        width = len(nums)
        nums.clear()
        nums.extend(self.num_to_list(nxt, width))

    def list_to_num(self, nums: List[int]) -> int:
        s = ''
        for i in nums:
            s += str(i)
        return int(s)

    def num_to_list(self, num, n) -> List[int]:
        return [int(i) for i in str(num).zfill(n)]

    def get_all_possible(self, nums: List[int]) -> List[int]:
        """
        >>> Solution().get_all_possible([1,2,3])
        [123, 132, 213, 231, 312, 321]
        """
        ans = []
        self.contact(ans, '', nums)
        ans.sort()
        return ans

    def contact(self, ans: List[int], pre, nums: List[int]):
        n = len(nums)
        if n == 1:
            ans.append(int(pre + str(nums[0])))
        else:
            for i in range(n):
                num = nums[i]
                nums.pop(i)
                self.contact(ans, pre + str(num), nums)
                nums.insert(i, num)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
