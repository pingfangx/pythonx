from typing import List

from leetcode import ListFactory


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        因为是有序的，很容易想到至少应该用二分法
        这里先基本遍历实现一遍，注意不能用 for in range() ，i 只在 range 范围内而不是每次判断

        查看讨论，在 1 中自己本来是想用二分法的，但是 while 不知道怎么判断，一直处理不出来
        使用 low <= high 判断，那么 low 要执行 + 1
        循环后 low 处表示一个最小的大于 target 的位置，比如 low 为 0 表示所有元素都大于 target，插入到 0 处

        使用这样的 while 退出时 low==high==mid
        为了防止死循环，需要 mid+1 和 mid -1

        时间复杂度怎么算
        需要 k 次 2^k=n，所以 k=log2(n)
        T(n)=O(log n)
        >>> Solution().searchInsert(ListFactory.from_num(123),0)
        0
        >>> Solution().searchInsert(ListFactory.from_num(123),3)
        2
        >>> Solution().searchInsert(ListFactory.from_num(124),3)
        2
        >>> Solution().searchInsert(ListFactory.from_num(123),4)
        3
        """
        low = 0
        high = len(nums) - 1
        mid = 0
        while low <= high:
            # mid = (low + high) // 2
            # 防止溢出
            mid += (high - low) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                # 如果小于 target，那么 low 至少为 mid+1
                low = mid + 1
            else:
                # 如果大于 target，如果发现 mid-1 实际 < target 后续的循环中会继续判断，再加回来
                high = mid - 1
        return low


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
