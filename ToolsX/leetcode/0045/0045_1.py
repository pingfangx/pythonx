from typing import List


class Solution:
    """20190812"""

    def jump(self, nums: List[int]) -> int:
        """
        很有意思的题
        需要注意的是，如果倒数第3个是 1 那肯定不能跳 2 到终点
        如果是 2 ，那就不用跳到倒数第2个，直接到终点
        [1,1,1]
        [2,1,1]
        超时，应该考虑可以一遍到达终点

        1
        https://leetcode.com/problems/jump-game-ii/discuss/18014/Concise-O(n)-one-loop-JAVA-solution-based-on-Greedy

        以 23114 为例
        jumps=cur_end=cur_farthest=0
        第一跳为 2，表示可以跳到 index 为 1-2，即 3 或 1
        循环到 i==2,cur_farthest =4
        表示，1-2 之间，有某一个最远可以跳至 4
        也就是 0跳1跳4

        2   3   1   1   4
        0   1   2   3   4
        一跳可以跳到 2
        在 1-2 间，cur_farthest 被置为 4 ，说明在 1-2 间，可以从某一位置再加一跳就跳到 4

        >>> Solution().jump([2,3,1,1,4])
        2
        """
        n = len(nums)
        jumps = cur_end = cur_farthest = 0
        for i in range(n - 1):  # 注意是 < n-1，当 ==n-1 时已经到达末尾，不需要再一跳
            cur_farthest = max(cur_farthest, i + nums[i])
            # 一跳可以跳到 cur_end，多一跳可以跳到 cur_farthest
            if i == cur_end:
                jumps += 1
                cur_end = cur_farthest
        return jumps


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
