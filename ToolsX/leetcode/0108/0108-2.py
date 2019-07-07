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

        2
        感觉可以用索引来完成

        分析时间复杂度
        取切片时称动元素为基本操作
        1/2 n
            1/4 n
                1/8 n
                1/8 n
            1/4 n
                1/8 n
                1/8 n
        1/2 n
            ...

        可以看到每一轮共有 k 个 1/k n
        所以每一轮为 n
        而轮数为 log(n) 所以 T(n)=O(n logn)

        分析空间复杂度
        输出的树不考虑，那临时占用的就只有 mid 变量，与结点数一致
        S(n)=O(n)
        """
        if not nums:
            return None
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        # 原数组中序遍历而来，所以左右各能组成树
        if 0 < mid:
            root.left = self.sortedArrayToBST(nums[:mid])
        if mid + 1 < len(nums):
            root.right = self.sortedArrayToBST(nums[mid + 1:])
        return root


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
