from typing import List

from leetcode import TreeNode


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        """
        分析了一下，除了 root 可能有 right 其余的都是 left

        0
        算法不正确，原因在于题目要求的树是 DFS
        [-10,-3,0,5,9]
        5 是 9 的下一层，如果右侧按顺序，就成了 5 在 9 的上一层

        1
        分析发现，既然是 DF，相当于两树合并起来
        还是不对，理解错题目了，是要求平衡二叉树
        """
        if not nums:
            return None
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        left = root
        for i in range(mid - 1, -1, -1):
            left.left = TreeNode(nums[i])
            left = left.left

        if len(nums) > 2:
            # 右侧树，从最后一个元倒退回去
            root.right = TreeNode(nums[-1])
            left = root.right
            for i in range(len(nums) - 2, mid, -1):
                left.left = TreeNode(nums[i])
                left = left.left
        return root


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
