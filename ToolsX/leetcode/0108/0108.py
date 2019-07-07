from typing import List

from leetcode import TreeNode


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        """
        分析了一下，除了 root 可能有 right 其余的都是 left

        0
        算法不正确，原因在于题目要求的树是 DF
        [-10,-3,0,5,9]
        5 是 9 的下一层，如果右侧按顺序，就成了 5 在 9 的上一层
        """
        if not nums:
            return None
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        left = root
        for i in range(mid - 1, -1, -1):
            left.left = TreeNode(nums[i])
            left = left.left
        right = root
        for i in range(mid + 1, len(nums)):
            right.right = TreeNode(nums[i])
            right = right.right
        return root


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
