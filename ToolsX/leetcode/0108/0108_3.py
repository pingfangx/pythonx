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

        3
        时间复杂度
        不用新建子数组，视取值创建结点的 node = TreeNode(nums[mid]) 为基本语句
        因为共创建 n 个结点，每个结点都会需要创建
        T(n)=O(n)

        空间复杂度
        与 0108_2 中一致，是 mid 变量，每轮创建一个 mid
        S(n)=O(log n)
        """
        if not nums:
            return None
        return self.sorted_array_to_bst(nums, 0, len(nums) - 1)

    def sorted_array_to_bst(self, nums, start, stop):
        if start <= stop:
            # 这里 + 1 保证如果对称的时候，取偏右，因为题目中数组是中序遍历的
            mid = start + (stop - start + 1) // 2
            node = TreeNode(nums[mid])
            node.left = self.sorted_array_to_bst(nums, start, mid - 1)
            node.right = self.sorted_array_to_bst(nums, mid + 1, stop)
            return node
        else:
            return None


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
